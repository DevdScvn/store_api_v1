from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper
from .product_dao import ProductDAO
from .schemas import SProductCreate, SProduct, SProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=SProductCreate)
async def create_product(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                         products: SProductCreate):
    return await ProductDAO.add(session=session, data=products)


@router.get("", response_model=Sequence[SProduct])
async def get_products_pagination(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                                  skip: int = 0, limit: int = 1):
    return await ProductDAO.find_all_product(session=session, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=SProductRead)
async def get_product_by_id(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
                            product_id: int):
    product = await ProductDAO.find_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# @router.put("/{product_id}", response_model=SProductCreate)
# async def update_product(session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
#                          product_id: int):
#     product = ProductDAO.update_product_by_id(session=session, product_id=product_id)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product

