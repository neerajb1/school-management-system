from flask import Blueprint, jsonify, request, g
from app.middleware.auth_decorators import login_required,require_active_account
from app.middleware.role_decorators import require_any_role
from .services import UserService

users_bp = Blueprint("users", __name__)
service = UserService()


@users_bp.route("/", methods=["GET"])
@login_required
@require_active_account
@require_any_role("ADMIN")
def list_users():
    return jsonify(
        service.list_users(current_user_id=g.current_user_id)
    ), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id: int):
    return jsonify(
        service.get_user(
            user_id=user_id,
            current_user_id=g.current_user_id,
        )
    ), 200


@users_bp.route("/", methods=["POST"])
@login_required
def create_user():
    payload = request.get_json(silent=True) or {}
    return jsonify(
        service.create_user(
            data=payload,
            current_user_id=g.current_user_id,
        )
    ), 201


@users_bp.route("/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id: int):
    payload = request.get_json(silent=True) or {}
    return jsonify(
        service.update_user(
            user_id=user_id,
            data=payload,
            current_user_id=g.current_user_id,
        )
    ), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@login_required
def deactivate_user(user_id: int):
    service.deactivate_user(
        user_id=user_id,
        current_user_id=g.current_user_id,
    )
    return "", 204
