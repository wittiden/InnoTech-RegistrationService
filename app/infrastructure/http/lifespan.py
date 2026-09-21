from contextlib import asynccontextmanager
from typing import AsyncGenerator

from loguru import logger
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info('Application - start')

    yield

    logger.info('Application - and')
