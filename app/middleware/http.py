import sys
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.utils.logging import AppLogger

logger = AppLogger().get_logger()


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        # response = time.time()
        process_time = time.time() - start_time
        logger.info(
            f"{request.client.host} - \"{request.method} {request.url.path } {request.scope['http_version']}\" {response.status_code} { process_time:.2f}s"
        )
        response = await call_next(request)
        return response
