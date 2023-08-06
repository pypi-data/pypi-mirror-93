from typing import Optional
from TwitchX.api import API
from TwitchX.helix.model import GetUsersResponse
from TwitchX.helix.model import GetUsersFollowsResponse


class Users:
    def __init__(self, source: API) -> None:
        self.method = "get"
        self.path = "users"
        self.source = source

    async def get_users(
            self,
            _id: Optional[str] = None,
            login: Optional[str] = None,
            ignore_cache: bool = False
    ) -> GetUsersResponse:
        """Gets information about one or more specified Twitch users. Users are identified by optional user IDs and/or login name

        :param _id: User ID. Multiple user IDs can be specified. Limit: 100.
        :param login: User login name. Multiple login names can be specified. Limit: 100.
        :param ignore_cache: Ignore Caching Option, default: False
        :return: GetUsersResponse
        """
        query = {}
        if _id:
            query["id"]: str = _id
        if login:
            query["login"]: str = login

        _users = await self.source.request(
            method=self.method,
            path=self.path,
            params=query,
            ignore_cache=ignore_cache
        )
        response = GetUsersResponse(**_users)
        return response

    async def get_users_follows(
            self,
            after: Optional[str] = None,
            first: Optional[int] = 20,
            from_id: Optional[str] = None,
            to_id: Optional[str] = None,
            ignore_cache: bool = False
    ) -> GetUsersFollowsResponse:
        """Gets information on follow relationships between two Twitch users. This can return information like “who is qotrok following,” “who is following qotrok,” or “is user X following user Y.” Information returned is sorted in order, most recent follow first.

        :param after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response. The cursor value specified here is from the pagination response field of a prior query.
        :param first: Maximum number of objects to return. Maximum: 100. Default: 20.
        :param from_id: User ID. The request returns information about users who are being followed by the from_id user.
        :param to_id: User ID. The request returns information about users who are following the to_id user.
        :param ignore_cache: Ignore Caching Option, default: False
        :return:
        """

        query: dict = {}
        if after:
            query["after"]: str = after
        if first:
            query["first"]: int = first
        if from_id:
            query["from_id"]: str = from_id
        if to_id:
            query["to_id"]: str = to_id

        _users = await self.source.request(
            method=self.method,
            path=self.path + "/follows",
            params=query,
            ignore_cache=ignore_cache
        )
        resp = GetUsersFollowsResponse(**_users)
        return resp




