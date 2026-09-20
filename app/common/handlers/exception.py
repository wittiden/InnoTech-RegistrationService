from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.common.handlers.base import BaseError


def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        content={
            'id': request.headers['X-Request-ID'],
            'path': request.base_url.path,
            'title': exc.title,
            'details': exc.details
        },
        status_code=exc.status_code,
    )
