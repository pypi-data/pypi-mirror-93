import re
import asyncio
from typing import Optional
from datetime import timedelta
from TwitchX.util import HTTPUtil
from TwitchX.cache import Cache


class GQL_CLIENT_ID(HTTPUtil):
    SHARED_CACHE: Cache = Cache()

    def __init__(
            self,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            cache_duration: Optional[timedelta] = None
    ):

        self.cache_duration: Optional[timedelta] = cache_duration
        self.static_id = "kimne78kx3ncx6brgo4mv6wki5h1ko"
        self._loop = loop or asyncio.get_event_loop()

        self._url = "https://twitch.tv"
        super(GQL_CLIENT_ID, self).__init__()
        self.ext = self

    async def _client_id_regex(self):
        regex = await self._loop.run_in_executor(None, re.compile, r'\"Client-ID\":\"([A-Za-z0-9]+)\"')
        return regex

    async def get_client_id(self):
        cache_key: str = f"gql-client-id"
        if GQL_CLIENT_ID.SHARED_CACHE.get(cache_key):
            return GQL_CLIENT_ID.SHARED_CACHE.get(cache_key)

        source = await self.ext.requests("GET", self._url, headers=self.ext.get_user_agent())
        reg = await self._client_id_regex()
        output = reg.findall(source)
        if output is None:
            return self.static_id

        client_id = output[0]

        GQL_CLIENT_ID.SHARED_CACHE.set(key=cache_key, value=client_id, duration=self.cache_duration)
        return client_id



