from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dao.base_dao import BaseDAO
from products.models import Product
from products.schemas import SProductRead


class ProductDAO(BaseDAO):
    model = Product

    @staticmethod
    async def find_all_product(session: AsyncSession, skip=0, limit=10):
        stmt = select(Product).order_by(Product.id).offset(skip).limit(limit)
        result = await session.scalars(stmt)
        return result.all()

    # @staticmethod
    # async def find_product_by_id(session: AsyncSession, product_id: int):
    #     query = select(Product).filter_by(product_id=product_id)
    #     result = await session.execute(query)
    #     return result.mappings().one_or_none()

    # async def find_product_by_id(session: AsyncSession, product_id: int):
    #     return await BaseDAO.find_one_or_none(session=session, product_id=product_id)

    @staticmethod
    async def find_product_by_id(session: AsyncSession, product_id: int) -> SProductRead:
        """Return product by id."""
        return await ProductDAO.get_object_or_404(session, id=product_id)

    @staticmethod
    async def update_product_by_id(session: AsyncSession, product_id: int):
        query = select(Product).filter(Product.id == product_id)
        if query:
            session.add(query)
        await session.commit()
        await session.refresh(query)
        return query
