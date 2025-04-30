from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from database import db_helper
from settings.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose_engine")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
