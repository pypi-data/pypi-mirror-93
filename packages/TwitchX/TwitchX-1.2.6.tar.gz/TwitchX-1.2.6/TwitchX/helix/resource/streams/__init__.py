from typing import Optional
from TwitchX.api import API
from TwitchX.helix.model import GetStreamsResponse


class Streams:
    def __init__(self, source: API):
        self.method = "get"
        self.path = "streams"
        self.source = source

    async def get_streams(
            self,
            after: Optional[str] = None,
            before: Optional[str] = None,
            first: Optional[int] = 20,
            game_id: Optional[str] = None,
            language: Optional[str] = None,
            user_id: Optional[str] = None,
            user_login: Optional[str] = None,
            ignore_cache: bool = False
    ) -> GetStreamsResponse:
        """Gets information about active streams. Streams are returned sorted by number of current viewers, in descending order.

        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response. The cursor value specified here is from the pagination response field of a prior query.
        :param before: Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response. The cursor value specified here is from the pagination response field of a prior query.
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :param game_id: Returns streams broadcasting a specified game ID. You can specify up to 100 IDs.
        :param language: Stream language. You can specify up to 100 languages. A language value must be either the ISO 639-1 two-letter code for a supported stream language or “other”.
        :param user_id: Returns streams broadcast by one or more specified user IDs. You can specify up to 100 IDs.
        :param user_login: Returns streams broadcast by one or more specified user login names. You can specify up to 100 names.
        :param ignore_cache: Ignore Caching Option, default: False
        :return: GetStreamsResponse
        """
        query = {}
        if first:
            query["first"] = first
        if after:
            query["after"] = after
        if before:
            query["before"] = before
        if game_id:
            query["game_id"] = game_id
        if language:
            query["language"] = language
        if user_id:
            query["user_id"] = user_id
        if user_login:
            query["user_login"] = user_login

        _streams = await self.source.request(
            method=self.method,
            path=self.path,
            params=query,
            ignore_cache=ignore_cache
        )
        resp = GetStreamsResponse(**_streams)
        return resp











