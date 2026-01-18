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

def require_active_account(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if g.current_account_status != "ACTIVE":
            return jsonify({
                "error": {
                    "code": "account_not_active",
                    "message": "Account onboarding not completed"
                }
            }), 403
        return fn(*args, **kwargs)
    return wrapper



