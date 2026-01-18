# app/core/exceptions.py

class AppError(Exception):
    """
    Base application error.
    """
    status_code = 400
    error_code = "bad_request"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class PermissionDenied(AppError):
    status_code = 403
    error_code = "permission_denied"


class NotAuthenticated(AppError):
    status_code = 401
    error_code = "not_authenticated"


class NotFound(AppError):
    status_code = 404
    error_code = "not_found"


class ValidationError(AppError):
    status_code = 400
    error_code = "validation_error"
