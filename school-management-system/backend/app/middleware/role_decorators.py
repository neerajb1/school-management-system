from functools import wraps
from flask import jsonify, g
from app.core.auth_utils import get_current_user
from .auth_decorators import login_required
from app.middleware.role_utils import get_current_user_role_name


def require_roles(*allowed_roles):
    """
    Usage:
        @require_roles("ADMIN")
        @require_roles("ADMIN", "TEACHER")
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Authentication check
            if not g.current_user_id:
                return jsonify({"error": "Authentication required"}), 401

            # Authorization check
            if not g.current_user_role or g.current_user_role not in allowed_roles:
                return jsonify({"error": "Forbidden"}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator

def require_any_role(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            user_id = g.current_user_id
            user_role = get_current_user_role_name(user_id)

            if user_role not in allowed_roles:
                return jsonify({
                    "error": "Forbidden",
                    "allowed_roles": list(allowed_roles)
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator