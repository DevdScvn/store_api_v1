import datetime
from typing import List

from pydantic import BaseModel

from order_items.schemas import SOrderItemCreate


class SOrder(BaseModel):
    status: str


class SOrderCreate(SOrder):
    items: List[SOrderItemCreate]


class SOrderRead(SOrder):
    id: int
    created_at: datetime.datetime


class SOrderReadID(SOrderCreate):
    id: int
    created_at: datetime.datetime
