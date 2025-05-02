from pydantic import BaseModel


class SOrderItem(BaseModel):
    order_id: int
    product_id: int
    amount: int
