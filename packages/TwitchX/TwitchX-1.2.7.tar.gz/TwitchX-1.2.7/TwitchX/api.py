import time
import aiohttp
from datetime import timedelta
from typing import Dict, Optional

from TwitchX.cache import Cache


class API:
    SHARED_CACHE: Cache = Cache()

    def __init__(
            self,
            base_url: Optional[str] = None,
            client_id: Optional[str] = None,
            use_cache: Optional[bool] = False,
            bearer_token: Optional[str] = None,
            cache_duration: Optional[timedelta] = None
    ) -> None:
        """
        Twitch API

        :param base_url: API URL
        :param client_id: Twitch Client ID
        :param use_cache: Use local cache
        :param bearer_token: OAuth Token
        :param cache_duration: Local cache duration
        """
        self.base_url: Optional[str] = base_url
        self.client_id: Optional[str] = client_id
        self.use_cache: bool = use_cache
        self.bearer_token: Optional[str] = bearer_token
        self.cache_duration: Optional[timedelta] = cache_duration

    def _headers(self) -> Dict[str, str]:
        default: Dict[str, str] = {}

        if self.client_id:
            default["Client-ID"] = self.client_id

        if self.bearer_token:
            default["Authorization"] = f"Bearer {self.bearer_token}"
        return default

    def _url(self, path: str = '') -> str:
        return self.base_url.rstrip('/') + '/' + path.lstrip('/')

    @staticmethod
    def flush_cache():
        API.SHARED_CACHE.flush()

    async def request(self, method: str, path: str = "", ignore_cache: bool = False, params= {}, **kwargs):
        url: str = self._url(path=path)
        async with aiohttp.ClientSession(headers=self._headers()) as session:
            if method.lower() == "get":
                async with session.get(url=url, params=params) as resp:
                    cache_key: str = f"{resp.method}:{resp.url}"
                    if self.use_cache and not ignore_cache and API.SHARED_CACHE.get(cache_key):
                        await session.close()
                        return API.SHARED_CACHE.get(cache_key)
                    if resp.status != 200:
                        resp.raise_for_status()
                    res = await resp.json()

            elif method.lower() == "post":
                async with session.post(url=url, **kwargs) as resp:
                    cache_key: str = f"{resp.method}:{resp.url}"
                    if self.use_cache and not ignore_cache and API.SHARED_CACHE.get(cache_key):
                        await session.close()
                        return API.SHARED_CACHE.get(cache_key)
                    if resp.status != 200:
                        resp.raise_for_status()
                    res = await resp.json()
        # Cache response
        if self.use_cache and not ignore_cache:
            API.SHARED_CACHE.set(key=cache_key, value=res, duration=self.cache_duration)
        return res
