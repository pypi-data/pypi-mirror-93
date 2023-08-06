from typing import Optional
from pydantic import BaseModel


class GetUsersParams(BaseModel):
    id: Optional[str] = None
    login: Optional[str] = None


class GetUsersFollowsParams(BaseModel):
    from_id: Optional[str]
    to_id: Optional[str]
    after: Optional[str]
    first: Optional[int]
