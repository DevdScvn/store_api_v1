import datetime

from pydantic import BaseModel


class SOrder(BaseModel):
    id: int
    created_at: datetime.datetime
    status: str


