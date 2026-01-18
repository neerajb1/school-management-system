from flask import Blueprint, jsonify, g
from app.middleware.auth_decorators import login_required
from app.middleware.role_decorators import require_roles, require_any_role
import logging

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    logger.info("Accessing index route", extra={"user_id": g.get("current_user_id")})
    try:
        return jsonify({"message": "Welcome to the School Management System API!"}), 200
    except Exception as e:
        logger.exception("Unexpected error in index route", extra={"user_id": g.get("current_user_id")})
        return jsonify({"error": "Internal server error"}), 500


@main_bp.route("/secure", methods=["GET"])
@login_required
def secure_endpoint():
    return {"ok": True, "user_id": g.current_user_id}

@main_bp.route("/admin-only", methods=["GET"])
@login_required
@require_roles("ADMIN")
def admin_only():
    return jsonify({"admin": True})


@main_bp.route("/staff-area")
@require_any_role("ADMIN", "TEACHER")
def staff_area():
    return jsonify({"ok": True, "role": "STAFF"})