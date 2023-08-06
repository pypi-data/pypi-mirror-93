from typing import List, Callable

from TwitchX.helix.model.users import GetUsersResponse
from TwitchX.helix.model.users import GetUsersFollowsResponse
from TwitchX.helix.model.streams import GetStreamsResponse

from TwitchX.helix.model.users.params import GetUsersParams
from TwitchX.helix.model.users.params import GetUsersFollowsParams
from TwitchX.helix.model.streams.params import GetStreamsParams

__all__: List[Callable] = [
    GetUsersResponse,
    GetUsersFollowsResponse,
    GetUsersParams,
    GetUsersFollowsParams,
    GetStreamsResponse,
    GetStreamsParams
]
