from fastapi.responses import JSONResponse
from fastapi.requests import Request


def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        content={
            'path': str(request.url.path),
            'title': exc.title,
            'details': exc.details
        },
        status_code=exc.status_code,
    )
