from pydantic import BaseModel
from typing import Optional, List
from TwitchX.helix.model.global_model import Cursor


class SearchChannelsDictionary(BaseModel):
    id: Optional[str] = None
    game_id: Optional[str] = None
    broadcaster_login: Optional[str] = None
    display_name: Optional[str] = None
    broadcaster_language: Optional[str] = None
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_live: bool
    started_at: Optional[str] = None
    tag_ids: Optional[List[str]]


class SearchCategoriesDictionary(BaseModel):
    box_art_url: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None


class SearchChannelsResponse(BaseModel):
    data: Optional[List[SearchChannelsDictionary]]
    pagination: Optional[Cursor]


class SearchCategoriesResponse(BaseModel):
    data: Optional[List[SearchCategoriesDictionary]]
    pagination: Optional[Cursor]

