from flask import Blueprint, jsonify, request, g
import logging

logger = logging.getLogger(__name__)

api_v1_bp = Blueprint('api_v1', __name__)

@api_v1_bp.before_request
def log_request_start():
    logger.info(
        "Request started",
        extra={
            "method": request.method,
            "path": request.path,
            "request_id": g.get("request_id"),
        },
    )

@api_v1_bp.after_request
def log_request_end(response):
    logger.info(
        "Request completed",
        extra={
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "request_id": g.get("request_id"),
        },
    )
    return response
