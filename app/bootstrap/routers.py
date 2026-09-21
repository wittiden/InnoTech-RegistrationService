from fastapi import FastAPI

from app.modules.auth.api.v1.routers.auth import auth_router
from app.modules.users.api.v1.routers.create import create_router
from app.modules.users.api.v1.routers.show import show_router

ROUTERS_LIST = [
    create_router,
    show_router,
    auth_router,
]


def setup_routers(app: FastAPI) -> None:
    for router in ROUTERS_LIST:
        app.include_router(router)
