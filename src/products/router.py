from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import db_helper
from .product_dao import ProductDAO
from .schemas import SProductCreate, SProduct, SProductRead, SProductDelete, SProductUpdatePartial

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=SProductCreate)
async def create_product(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                         products: SProductCreate):
    """
    Добавляет новый продукт.

    Параметры:
    - products: Данные для добавления (тело запроса)

    Возвращает:
    - Объект продукта
    """
    return await ProductDAO.add(session=session, data=products)


@router.get("", response_model=Sequence[SProductRead])
@cache(expire=60)
async def get_products_pagination(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                                  skip: int = 0, limit: int = 10):
    """
    Находит все продукты.

    Параметры:
    - skip и limit: Для пагинации

    Возвращает:
    - Объект продукта
    """
    return await ProductDAO.find_all_product(session=session, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=SProductRead)
async def get_product_by_id(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                            product_id: int):
    """
    Находит продукт по id.

    Параметры:
    - product_id: Данные для добавления по id (тело запроса)

    Возвращает:
    - Объект продукта
    - 404 если продукт не найден
    """
    product = await ProductDAO.find_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=SProductRead)
async def update_product(
        product_id: int,
        product_update: SProductCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    """
    Обновляет информацию о продукте

    Параметры:
    - product_id: ID продукта для обновления
    - product_update: Данные для обновления (тело запроса)

    Возвращает:
    - Обновленный объект продукта
    - 404 если продукт не найден
    """
    db_product = await ProductDAO.update_product(session, product_id=product_id, product_update=product_update)

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    return db_product


@router.patch("/{product_id}", response_model=SProductRead)
async def update_product(
        product_id: int,
        product_update: SProductUpdatePartial,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    """
    Частично обновляет информацию о продукте (PATCH)

    Позволяет обновить отдельные поля товара.
    Не требует передачи всех полей, только те, которые нужно изменить.

    Параметры:
    - product_id: ID продукт для обновления
    - product_update: Данные для обновления (тело запроса)

    Возвращает:
    - Обновленный объект продукт
    - 404 если продукт не найден
    """
    db_product = await ProductDAO.update_product(session=session,
                                                 product_id=product_id,
                                                 product_update=product_update,
                                                 partial=True)

    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

    return db_product


@router.delete("/delete/{}")
async def delete_product_by_id(
        product_id: SProductDelete,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    """
    Позволяет удалить продукт по id.
    Не требует передачи всех полей, только id.

    Параметры:
    - product_id: ID продукт для обновления.

    Возвращает:
    - Сообщение, что продукт удален.
    """
    await ProductDAO.del_one(session, id=product_id.id)
    return {"message": f"Продукт № {product_id.id} удален"}
