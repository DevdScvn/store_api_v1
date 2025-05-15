from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from order_items.models import OrderItem
from orders.models import Order
from orders.schemas import SOrderCreate
from products.models import Product


class InsufficientStockException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Insufficient stock for product {product_id}")


async def create_order_with_items(
        session: AsyncSession,
        order_data: SOrderCreate
) -> Order:
    """
    Создание нового заказа с проверкой наличия товаров
    и расчетом общей суммы
    """
    # Проверка наличия товаров и расчет позиций
    order_items = []

    for item in order_data.items:
        # Получаем товар из БД
        product = await session.get(Product, item.product_id)
        if not product or product.amount < item.amount:
            raise InsufficientStockException(product_id=item.product_id)

        order_items.append(OrderItem(
            product_id=item.product_id,
            amount=item.amount,
        ))

    # Создаем заказ
    db_order = Order(
        status=order_data.status,
    )
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)

    # Добавляем позиции с ссылкой на заказ
    for item in order_items:
        item.order_id = db_order.id
        session.add(item)

        # Обновляем остатки товара
        product = await session.get(Product, item.product_id)
        product.amount -= item.amount

    await session.commit()
    await session.refresh(db_order)
    return db_order


async def list_orders(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 10
) -> Order:
    """Список заказов с пагинацией"""
    result = await session.execute(
        select(Order)
        .offset(skip)
        .limit(limit)
        .order_by(Order.created_at.desc())
    )
    return result.scalars().all()


async def get_order_with_items(
    session: AsyncSession,
    order_id: int
) -> Order | None:
    """Получение заказа со всеми позициями"""
    result = await session.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    return result.scalars().first()
