from flask import Blueprint, jsonify
from app.middleware.auth_decorators import login_required
from app.middleware.role_decorators import require_any_role
from .services import list_users_service

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@login_required
@require_any_role('ADMIN')
def list_users():
    users = list_users_service()
    return jsonify(users), 200

