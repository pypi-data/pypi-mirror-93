from typing import Optional
from pydantic import BaseModel


class GetStreamsParams(BaseModel):
    after: Optional[str] = None
    before: Optional[str] = None
    first: Optional[int] = None
    game_id: Optional[str] = None
    language: Optional[str] = None
    user_id: Optional[str] = None
    user_login: Optional[str] = None
