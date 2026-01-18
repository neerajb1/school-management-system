from functools import wraps
from flask import g, jsonify
from app.middleware.role_utils import get_current_user_role_name


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not g.get("current_user_id"):
            return jsonify({"error": "Authentication required"}), 401
        return fn(*args, **kwargs)
    return wrapper




