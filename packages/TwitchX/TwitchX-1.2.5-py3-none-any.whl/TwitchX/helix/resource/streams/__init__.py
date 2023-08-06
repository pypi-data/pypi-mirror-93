from TwitchX.api import API
from TwitchX.helix.model import GetStreamsResponse


class Streams:
    def __init__(self, source: API):
        self.method = "get"
        self.path = "streams"
        self.source = source

    async def get_streams(self, params: dict, ignore_cache=False) -> GetStreamsResponse:
        _streams = await self.source.request(
            method=self.method,
            path=self.path,
            params=params,
            ignore_cache=ignore_cache
        )
        resp = GetStreamsResponse(**_streams)
        return resp











