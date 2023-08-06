from typing import List, Callable

from TwitchX.helix.model.users import GetUsersResponse
from TwitchX.helix.model.users import GetUsersFollowsResponse
from TwitchX.helix.model.streams import GetStreamsResponse
from TwitchX.helix.model.search import SearchChannelsResponse
from TwitchX.helix.model.search import SearchCategoriesResponse


__all__: List[Callable] = [
    GetUsersResponse,
    GetUsersFollowsResponse,
    GetStreamsResponse,
    SearchChannelsResponse,
    SearchCategoriesResponse
]
