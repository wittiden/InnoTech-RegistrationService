from fastapi import FastAPI

from app.infrastructure.http.middlewares.logger import LoggerMiddleware
from app.infrastructure.http.middlewares.timeout import TimeoutMiddleware

MIDDLEWARES_LIST = [
    LoggerMiddleware,
    TimeoutMiddleware,
]


def setup_middlewares(app: FastAPI) -> None:
    for middleware in  MIDDLEWARES_LIST:
        app.add_middleware(middleware)
