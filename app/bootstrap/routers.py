from fastapi import FastAPI

from app.modules.auth.api.v1.routers.auth import auth_router

ROUTERS_LIST = [
    auth_router,
]


def setup_routers(app: FastAPI) -> None:
    for router in ROUTERS_LIST:
        app.include_router(router)
