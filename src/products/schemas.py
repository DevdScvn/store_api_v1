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


class SProductUpdate(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    amount: int


class SProductUpdatePartial(SProductCreate):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    amount: int | None = None


class SProductDelete(BaseModel):
    id: int
