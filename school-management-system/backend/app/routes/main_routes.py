from flask import Blueprint, jsonify,g
from app.middleware.auth_decorators import login_required
from app.middleware.role_decorators import require_roles,require_any_role

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the School Management System API!"}), 200


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