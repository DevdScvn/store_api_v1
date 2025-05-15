from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Sequence

from database import db_helper
from orders import order_dao
from orders.schemas import SOrderRead, SOrderCreate, SOrderReadID

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/",
    response_model=SOrderRead,
)
async def create_order(
        order_data: SOrderCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    """
    Создание нового заказа с проверкой наличия товаров.

    - Проверяет доступное количество каждого товара
    - Резервирует товары при успешном создании
    - Рассчитывает общую сумму заказа
    """
    try:
        return await order_dao.create_order_with_items(session, order_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недостаточно товара с ID на складе"
        )


@router.get("/", response_model=Sequence[SOrderRead])
async def read_orders(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    skip: int = 0,
    limit: int = 10,
):
    """Получение списка заказов с пагинацией"""
    return await order_dao.list_orders(session, skip=skip, limit=limit)


@router.get(
    "/{order_id}",
    response_model=SOrderReadID,
    summary="Получить детали заказа"
)
async def read_order(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_id: int,
):
    """Получение полной информации о заказе с позициями"""
    db_order = await order_dao.get_order_with_items(session, order_id=order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    return db_order
