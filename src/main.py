import logging

from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from prometheus_fastapi_instrumentator import Instrumentator

from database import db_helper
from settings.config import settings


from products.router import router as product_router
from orders.router import router as order_router
from importer.router import router as file_router

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    redis = aioredis.from_url("redis://localhost:6379", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # shutdown
    log.warning("dispose_engine")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)

main_app.include_router(product_router)
main_app.include_router(file_router)
main_app.include_router(order_router)


instrumentator = (
    Instrumentator(
        should_group_status_codes=False,
        excluded_handlers=[".*admin.*", "/metrics"],
    )
    .instrument(main_app)
    .expose(main_app)
)


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
