from pydantic import BaseModel


class SProduct(BaseModel):
    name: str
    description: str | None = None
    price: float
    amount: int


class SProductCreate(SProduct):
    pass


class SProductRead(SProduct):
    id: int
