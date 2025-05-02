from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession):
        stmt = select(cls.model).order_by(cls.model.id)
        result = await session.scalars(stmt)
        return result.all()

        # stmt = select(User).order_by(User.id)
        # result = await session.scalars(stmt)
        # return result.all()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def add(cls, data, session: AsyncSession) -> model:
        query = cls.model(**data.model_dump())
        session.add(query)
        await session.commit()
        await session.refresh(query)
        return query

    @classmethod
    async def get_object_or_404(cls, db: AsyncSession, **filter_params):
        """
        Get one object from the table.

        If no object found raise 404.
        """
        query = select(cls.model).filter_by(**filter_params)
        result = await db.execute(query)
        if result := result.unique().scalar_one_or_none():
            return result
        else:
            raise HTTPException(status_code=404, detail="Object not found")
