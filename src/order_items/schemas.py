from pydantic import BaseModel


class SOrderItem(BaseModel):
    product_id: int
    amount: int


class SOrderItemCreate(SOrderItem):
    pass


class SOrderItemRead(SOrderItem):
    id: int
    order_id: int

    class Config:
        from_attributes = True
