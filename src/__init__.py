from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.main import sessionmanager
from src.config import Config
from src.auth.routers import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title=Config.PROJECT_NAME,
    version=Config.VERSION,
    description='A REST API for Book service with reviews.'
)


app.include_router(
    auth_router, prefix=f'/api/{Config.VERSION}/auth', tags=['auth']
)
