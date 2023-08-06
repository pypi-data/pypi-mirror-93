from TwitchX.api import API
from TwitchX.helix.model import GetUsersResponse
from TwitchX.helix.model import GetUsersFollowsResponse



class Users:
    def __init__(self, source: API):
        self.method = "get"
        self.path = "users"
        self.source = source

    async def get_users(self, params: dict, ignore_cache=False) -> GetUsersResponse:
        """Gets information about one or more specified Twitch users.
        Users are identified by optional user IDs and/or login name.
        If neither a user ID nor a login name is specified, the user is looked up by Bearer token

        :param params: Query Parameters
        :param ignore_cache: Ignore Caching Option, default: False
        :return: GetUsersResponse
        """
        par = params
        _users = await self.source.request(
            method=self.method,
            path=self.path,
            params=par,
            ignore_cache=ignore_cache
        )
        response = GetUsersResponse(**_users)
        return response

    async def get_users_follows(self, params: dict, ignore_cache=False) -> GetUsersFollowsResponse:
        """Gets information on follow relationships between two Twitch users.
        This can return information like “who is qotrok following,”
        “who is following qotrok,” or “is user X following user Y.”
        Information returned is sorted in order, most recent follow first.

        :param params: Query Parameters
        :param ignore_cache: Ignore Caching Option, default: False
        :return: GetUsersFollowsResponse
        """
        par = params
        _users = await self.source.request(
            method=self.method,
            path=self.path + "/follows",
            params=par,
            ignore_cache=ignore_cache
        )
        resp = GetUsersFollowsResponse(**_users)
        return resp




