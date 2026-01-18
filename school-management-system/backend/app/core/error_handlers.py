# app/core/error_handlers.py

from flask import jsonify
from app.core.exceptions import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        response = {
            "error": {
                "code": error.error_code,
                "message": error.message,
            }
        }
        return jsonify(response), error.status_code

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "error": {
                "code": "not_found",
                "message": "Resource not found",
            }
        }), 404

    @app.errorhandler(500)
    def handle_500(error):
        # Do NOT leak internals
        return jsonify({
            "error": {
                "code": "internal_server_error",
                "message": "An unexpected error occurred",
            }
        }), 500
