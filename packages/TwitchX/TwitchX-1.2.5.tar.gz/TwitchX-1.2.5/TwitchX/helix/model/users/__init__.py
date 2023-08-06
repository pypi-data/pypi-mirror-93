from typing import List, Optional
from pydantic import BaseModel
from TwitchX.helix.model.global_model import Cursor


class GetUsersDictionary(BaseModel):
    id: Optional[str]
    login: Optional[str]
    display_name: Optional[str]
    type: Optional[str]
    broadcaster_type: Optional[str]
    description: Optional[str]
    profile_image_url: Optional[str]
    offline_image_url: Optional[str]
    view_count: Optional[int]
    email: Optional[str]
    created_at: Optional[str]


class GetUsersFollowsDictionary(BaseModel):
    from_id: Optional[str]
    from_login: Optional[str]
    from_name: Optional[str]
    to_id: Optional[str]
    to_name: Optional[str]
    followed_at: Optional[str]


class GetUsersResponse(BaseModel):
    data: Optional[List[GetUsersDictionary]]


class GetUsersFollowsResponse(BaseModel):
    total: Optional[int]
    data: Optional[List[GetUsersFollowsDictionary]]
    pagination: Optional[Cursor]


__all__ = [GetUsersResponse, GetUsersFollowsResponse]





