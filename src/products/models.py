from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from order_items.models import OrderItem


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[str]
    price: Mapped[float] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(default=0, nullable=False)
    # order_item: Mapped["OrderItem"] = relationship("OrderItem", back_populates="orders")
