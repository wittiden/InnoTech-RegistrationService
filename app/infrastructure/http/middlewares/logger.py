from time import perf_counter
from uuid import uuid4

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class LoggerMiddleware(BaseHTTPMiddleware):
    """Middleware логирования HTTP ответов"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = uuid4()
        start_time = perf_counter()

        response = await call_next(request)

        if not request.url.path.startswith('/api/v1'):
            return response

        process_time = (perf_counter() - start_time) * 1000
        process_time_str = f'{process_time:.2f} ms'
        log_srt = f'{request_id} | {request.url.path} | {response.status_code} | {process_time_str}'

        if 200 <= response.status_code < 300:
            logger.info(log_srt)
        elif 400 <= response.status_code < 500:
            logger.warning(log_srt)
        elif 500 <= response.status_code < 600:
            logger.error(log_srt)

        response.headers['X-Request-ID'] = str(request_id)
        response.headers['X-Process-Time'] = process_time_str

        return response
