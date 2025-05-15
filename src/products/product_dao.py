from functools import partial

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from dao.base_dao import BaseDAO
from products.models import Product
from products.schemas import SProductRead, SProduct


class ProductDAO(BaseDAO):
    model = Product

    @staticmethod
    async def find_all_product(session: AsyncSession, skip=0, limit=10):
        stmt = select(Product).order_by(Product.id).offset(skip).limit(limit)
        result = await session.scalars(stmt)
        return result.all()

    @staticmethod
    async def find_product_by_id(session: AsyncSession, product_id: int) -> SProductRead:
        return await ProductDAO.get_object_or_404(session, id=product_id)

    @staticmethod
    async def update_product(
            session: AsyncSession,
            product_id: int,
            product_update: SProduct,
            partial: bool = False,
    ) -> Product | None:
        result = await session.execute(select(Product).filter(Product.id == product_id))
        db_product = result.scalars().first()
        if not db_product:
            return None
        update_data = product_update.dict(exclude_unset=partial)
        for field, value in update_data.items():
            setattr(db_product, field, value)

        await session.commit()
        await session.refresh(db_product)
        return db_product
