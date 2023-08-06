from typing import Optional, List, Dict
from pydantic import BaseModel
from TwitchX.helix.model.global_model import Cursor


class GetStreamsDictionary(BaseModel):
    id: str
    user_id: str
    user_login: str
    user_name: str
    game_id: str
    type: str
    title: str
    view_count: int
    started_at: str
    language: str
    thumbnail_url: str


class GetStreamsTagID(BaseModel):
    tag_ids: List[str]


class GetStreamsResponse(BaseModel):
    data: Optional[List[Dict[GetStreamsDictionary, GetStreamsTagID]]]
    pagination: Optional[Cursor]


__all__ = [GetStreamsResponse]


















