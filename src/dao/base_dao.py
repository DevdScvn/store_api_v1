import logging

from fastapi import HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_helper

log = logging.getLogger(__name__)


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

    @classmethod
    async def add_bulk(cls, *data):
        """
        Для загрузки массива данных [{"id": 1}, {"id": 2}]
        Обрабатывает его через позиционные аргументы *args.
        """
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            async with db_helper.session_factory() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot bulk insert data into table"

            log.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def get_excel_table(cls):
        async with db_helper.session_factory() as session:
            result = await session.execute(select(cls.model))
            objects = result.scalars().all()
            return [
                {c.name: getattr(obj, c.name) for c in cls.model.__table__.columns}
                for obj in objects
            ]

    @classmethod
    async def del_one(cls, session: AsyncSession, **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        await session.execute(query)
        await session.commit()
