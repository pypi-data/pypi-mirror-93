from typing import Optional
from TwitchX.api import API
from TwitchX.error import RequiredQueryParameters
from TwitchX.helix.model import SearchChannelsResponse
from TwitchX.helix.model import SearchCategoriesResponse


class Search:
    def __init__(self, source: API):
        self.method = "get"
        self.path = "search"
        self.source = source

    async def channels(
            self,
            query: str,
            first: Optional[int] = 20,
            after: Optional[str] = None,
            live_only: bool = False,
            ignore_cache: bool = False
    ) -> SearchChannelsResponse:
        """
        Returns a list of channels (users who have streamed within the past 6 months)
        that match the query via channel name or description either entirely or partially.

        :param query: URl encoded search query
        :param first: Maximum number of objects to return. Maximum: 100 Default: 20
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response. The cursor value specified here is from the pagination response field of a prior query.
        :param live_only: Filter results for live streams only. Default: false
        :param ignore_cache: Ignore Caching Option, default: False
        :return: SearchChannelsResponse
        """
        if not query:
            raise RequiredQueryParameters

        params = {"query": query, "live_only": live_only}

        if first:
            params["first"]: int = first

        if after:
            params["after"]: str = after

        _channels = await self.source.request(
            method=self.method,
            path=self.path + "/channels",
            params=params,
            ignore_cache=ignore_cache
        )
        resp = SearchChannelsResponse(**_channels)
        return resp

    async def categories(
            self,
            query: str,
            first: Optional[int] = 20,
            after: Optional[str] = None,
            ignore_cache: bool = False
    ) -> SearchCategoriesResponse:
        """Returns a list of games or categories that match the query via name either entirely or partially.

        :param query: URl encoded search query
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response. The cursor value specified here is from the pagination response field of a prior query.
        :param ignore_cache: Ignore Caching Option, default: False
        :return: SearchCategoriesResponse
        """
        if not query:
            raise RequiredQueryParameters

        params: dict = {"query": query}
        if first:
            params["first"]: int = first
        if after:
            params["after"]: str = after

        resp = await self.source.request(
            self.method,
            self.path + "/categories",
            params=params,
            ignore_cache=ignore_cache
        )
        resp = SearchCategoriesResponse(**resp)
        return resp



