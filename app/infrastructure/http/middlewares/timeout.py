import asyncio
from asyncio import TimeoutError

from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse


class TimeoutMiddleware(BaseHTTPMiddleware):
    """Middleware контроля времени HTTP ответов"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await asyncio.wait_for(call_next(request), 15)
        except TimeoutError:
            return JSONResponse(
                content={
                    'path': request.url.path,
                    'title': 'Gateway timeout error',
                    'details': 'Waif for timeout error in middleware',
                },
                status_code=status.HTTP_504_GATEWAY_TIMEOUT
            )

        return response
