import datetime
import enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from order_items.models import OrderItem


class OrderStatus(enum.Enum):
    in_progress = "in_progress"
    delivered = "delivered"
    sent = "sent"


class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[OrderStatus]
    # order_item: Mapped["OrderItem"] = relationship("OrderItem", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
