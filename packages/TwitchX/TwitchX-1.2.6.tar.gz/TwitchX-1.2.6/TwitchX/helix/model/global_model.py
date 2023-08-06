from pydantic import BaseModel


class Cursor(BaseModel):
    cursor: str
