import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import db_helper
from settings.config import settings


from products.router import router as product_router
from importer.router import router as file_router

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    log.warning("dispose_engine")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)

main_app.include_router(product_router)
main_app.include_router(file_router)


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
