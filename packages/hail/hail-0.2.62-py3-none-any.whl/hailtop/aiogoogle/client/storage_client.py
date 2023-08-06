import os
from typing import Tuple, Any, Set, Optional, Mapping, Dict, AsyncIterator, cast, Type
from types import TracebackType
import asyncio
import urllib.parse
import aiohttp
from hailtop.aiotools import (
    FileStatus, FileListEntry, ReadableStream, WritableStream, AsyncFS,
    FeedableAsyncIterable, FileAndDirectoryError, MultiPartCreate)
from multidict import CIMultiDictProxy  # pylint: disable=unused-import
from .base_client import BaseClient


class PageIterator:
    def __init__(self, client: 'BaseClient', path: str, request_kwargs: Mapping[str, Any]):
        if 'params' in request_kwargs:
            request_params = request_kwargs['params']
            del request_kwargs['params']
        else:
            request_params = {}
        self._client = client
        self._path = path
        self._request_params = request_params
        self._request_kwargs = request_kwargs
        self._page = None

    def __aiter__(self) -> 'PageIterator':
        return self

    async def __anext__(self):
        if self._page is None:
            assert 'pageToken' not in self._request_params
            self._page = await self._client.get(self._path, params=self._request_params, **self._request_kwargs)
            return self._page

        next_page_token = self._page.get('nextPageToken')
        if next_page_token is not None:
            self._request_params['pageToken'] = next_page_token
            self._page = await self._client.get(self._path, params=self._request_params, **self._request_kwargs)
            return self._page

        raise StopAsyncIteration


class InsertObjectStream(WritableStream):
    def __init__(self, it, request_task):
        super().__init__()
        self._it = it
        self._request_task = request_task
        self._value = None

    async def write(self, b):
        assert not self.closed
        await self._it.feed(b)
        return len(b)

    async def _wait_closed(self):
        await self._it.stop()
        async with await self._request_task as resp:
            self._value = await resp.json()


class GetObjectStream(ReadableStream):
    def __init__(self, resp):
        super().__init__()
        self._resp = resp
        self._content = resp.content

    async def read(self, n: int = -1) -> bytes:
        assert not self._closed
        return await self._content.read(n)

    def headers(self) -> 'CIMultiDictProxy[str]':
        return self._resp.headers

    async def _wait_closed(self) -> None:
        self._content = None
        self._resp.release()
        self._resp = None


class StorageClient(BaseClient):
    def __init__(self, **kwargs):
        super().__init__('https://storage.googleapis.com/storage/v1', **kwargs)

    # docs:
    # https://cloud.google.com/storage/docs/json_api/v1

    async def insert_object(self, bucket: str, name: str, **kwargs) -> InsertObjectStream:
        if 'params' in kwargs:
            params = kwargs['params']
        else:
            params = {}
            kwargs['params'] = params
        assert 'name' not in params
        params['name'] = name
        assert 'uploadType' not in params
        params['uploadType'] = 'media'

        assert 'data' not in kwargs
        it: FeedableAsyncIterable[bytes] = FeedableAsyncIterable()
        kwargs['data'] = aiohttp.AsyncIterablePayload(it)
        request_task = asyncio.ensure_future(self._session.post(
            f'https://storage.googleapis.com/upload/storage/v1/b/{bucket}/o',
            **kwargs))
        return InsertObjectStream(it, request_task)

    async def get_object(self, bucket: str, name: str, **kwargs) -> GetObjectStream:
        if 'params' in kwargs:
            params = kwargs['params']
        else:
            params = {}
            kwargs['params'] = params
        assert 'alt' not in params
        params['alt'] = 'media'

        resp = await self._session.get(
            f'https://storage.googleapis.com/storage/v1/b/{bucket}/o/{urllib.parse.quote(name, safe="")}', **kwargs)
        return GetObjectStream(resp)

    async def get_object_metadata(self, bucket: str, name: str, **kwargs) -> Dict[str, str]:
        params = kwargs.get('params')
        assert not params or 'alt' not in params
        return cast(Dict[str, str], await self.get(f'/b/{bucket}/o/{urllib.parse.quote(name, safe="")}', **kwargs))

    async def delete_object(self, bucket: str, name: str, **kwargs) -> None:
        await self.delete(f'/b/{bucket}/o/{urllib.parse.quote(name, safe="")}', **kwargs)

    async def list_objects(self, bucket: str, **kwargs) -> PageIterator:
        return PageIterator(self, f'/b/{bucket}/o', kwargs)


class GetObjectFileStatus(FileStatus):
    def __init__(self, items: Dict[str, str]):
        self._items = items

    async def size(self) -> int:
        return int(self._items['size'])

    async def __getitem__(self, key: str) -> str:
        return self._items[key]


class GoogleStorageFileListEntry(FileListEntry):
    def __init__(self, url: str, items: Optional[Dict[str, Any]]):
        assert url.endswith('/') == (items is None), f'{url} {items}'
        self._url = url
        self._items = items
        self._status = None

    def name(self) -> str:
        parsed = urllib.parse.urlparse(self._url)
        return os.path.basename(parsed.path)

    async def url(self) -> str:
        return self._url

    def url_maybe_trailing_slash(self) -> str:
        return self._url

    async def is_file(self) -> bool:
        return self._items is not None

    async def is_dir(self) -> bool:
        return self._items is None

    async def status(self) -> FileStatus:
        if self._status is None:
            if self._items is None:
                raise ValueError("directory has no file status")
            self._status = GetObjectFileStatus(self._items)
        return self._status


class GoogleStorageMultiPartCreate(MultiPartCreate):
    def __init__(self, fs, url, num_parts):
        self._fs = fs
        self._url = url
        self._num_parts = num_parts

    async def create_part(self, number: int, start: int):
        raise NotImplementedError

    async def __aenter__(self) -> 'GoogleStorageMultiPartCreate':
        raise NotImplementedError

    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException],
                        exc_tb: Optional[TracebackType]) -> None:
        raise NotImplementedError


class GoogleStorageAsyncFS(AsyncFS):
    def __init__(self, storage_client: Optional[StorageClient] = None):
        if not storage_client:
            storage_client = StorageClient()
        self._storage_client = storage_client

    def schemes(self) -> Set[str]:
        return {'gs'}

    @staticmethod
    def _get_bucket_name(url: str) -> Tuple[str, str]:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != 'gs':
            raise ValueError(f"invalid scheme, expected gs: {parsed.scheme}")

        name = parsed.path
        if name:
            assert name[0] == '/'
            name = name[1:]

        return (parsed.netloc, name)

    async def open(self, url: str) -> ReadableStream:
        bucket, name = self._get_bucket_name(url)
        return await self._storage_client.get_object(bucket, name)

    async def create(self, url: str) -> WritableStream:
        bucket, name = self._get_bucket_name(url)
        return await self._storage_client.insert_object(bucket, name)

    async def multi_part_create(self, url: str, num_parts: int) -> GoogleStorageMultiPartCreate:
        return GoogleStorageMultiPartCreate(self, url, num_parts)

    async def staturl(self, url: str) -> str:
        assert not url.endswith('/')

        async def with_exception(f, *args, **kwargs):
            try:
                return (await f(*args, **kwargs)), None
            except Exception as e:
                return None, e

        [(is_file, isfile_exc), (is_dir, isdir_exc)] = await asyncio.gather(
            with_exception(self.isfile, url), with_exception(self.isdir, url + '/'))
        # raise exception deterministically
        if isfile_exc:
            raise isfile_exc
        if isdir_exc:
            raise isdir_exc

        if is_file:
            if is_dir:
                raise FileAndDirectoryError(url)
            return AsyncFS.FILE

        if is_dir:
            return AsyncFS.DIR

        raise FileNotFoundError(url)

    async def mkdir(self, url: str) -> None:
        pass

    async def makedirs(self, url: str, exist_ok: bool = False) -> None:
        pass

    async def statfile(self, url: str) -> GetObjectFileStatus:
        try:
            bucket, name = self._get_bucket_name(url)
            return GetObjectFileStatus(await self._storage_client.get_object_metadata(bucket, name))
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise FileNotFoundError(url) from e
            raise

    async def _listfiles_recursive(self, bucket: str, name: str) -> AsyncIterator[FileListEntry]:
        assert name.endswith('/')
        params = {
            'prefix': name
        }
        async for page in await self._storage_client.list_objects(bucket, params=params):
            prefixes = page.get('prefixes')
            assert not prefixes

            items = page.get('items')
            if items is not None:
                for item in page['items']:
                    yield GoogleStorageFileListEntry(f'gs://{bucket}/{item["name"]}', item)

    async def _listfiles_flat(self, bucket: str, name: str) -> AsyncIterator[FileListEntry]:
        assert name.endswith('/')
        params = {
            'prefix': name,
            'delimiter': '/',
            'includeTrailingDelimiter': 'true'
        }
        async for page in await self._storage_client.list_objects(bucket, params=params):
            prefixes = page.get('prefixes')
            if prefixes:
                for prefix in prefixes:
                    assert prefix.endswith('/')
                    url = f'gs://{bucket}/{prefix}'
                    yield GoogleStorageFileListEntry(url, None)

            items = page.get('items')
            if items:
                for item in page['items']:
                    yield GoogleStorageFileListEntry(f'gs://{bucket}/{item["name"]}', item)

    async def listfiles(self, url: str, recursive: bool = False) -> AsyncIterator[FileListEntry]:
        bucket, name = self._get_bucket_name(url)
        if not name.endswith('/'):
            name = f'{name}/'

        if recursive:
            it = self._listfiles_recursive(bucket, name)
        else:
            it = self._listfiles_flat(bucket, name)

        it = it.__aiter__()
        try:
            first_entry = await it.__anext__()
        except StopAsyncIteration:
            raise FileNotFoundError(url)  # pylint: disable=raise-missing-from

        async def cons(first_entry, it):
            yield first_entry
            try:
                while True:
                    yield await it.__anext__()
            except StopAsyncIteration:
                pass

        return cons(first_entry, it)

    async def isfile(self, url: str) -> bool:
        try:
            bucket, name = self._get_bucket_name(url)
            await self._storage_client.get_object_metadata(bucket, name)
            return True
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                return False
            raise

    async def isdir(self, url: str) -> bool:
        bucket, name = self._get_bucket_name(url)
        assert name.endswith('/')
        params = {
            'prefix': name,
            'delimiter': '/',
            'includeTrailingDelimiter': 'true',
            'maxResults': 1
        }
        async for page in await self._storage_client.list_objects(bucket, params=params):
            prefixes = page.get('prefixes')
            items = page.get('items')
            return prefixes or items
        assert False  # unreachable

    async def remove(self, url: str) -> None:
        bucket, name = self._get_bucket_name(url)
        await self._storage_client.delete_object(bucket, name)

    async def rmtree(self, url: str) -> None:
        try:
            async for entry in await self.listfiles(url, recursive=True):
                await self.remove(await entry.url())
        except FileNotFoundError:
            pass

    async def close(self) -> None:
        await self._storage_client.close()
        self._storage_client = None
