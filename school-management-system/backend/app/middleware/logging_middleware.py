import time
from flask import g, request
import logging

logger = logging.getLogger(__name__)

def logging_middleware(app):
    @app.before_request
    def start_timer():
        g.start_time = time.time()
        g.request_id = request.headers.get("X-Request-ID", "unknown")
        logger.info(
            "Request received",
            extra={
                "method": request.method,
                "path": request.path,
                "request_id": g.request_id,
                "user_id": g.get("current_user_id"),
            },
        )

    @app.after_request
    def log_response(response):
        duration_ms = (time.time() - g.start_time) * 1000
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "request_id": g.request_id,
                "user_id": g.get("current_user_id"),
            },
        )
        return response
