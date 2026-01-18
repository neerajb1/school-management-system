#!/usr/bin/env bash
set -euo pipefail

# --------------------------------------------------
# Base directory = backend/
# --------------------------------------------------
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Backend base: $BASE_DIR"

# --------------------------------------------------
# Helper: write file only if missing
# --------------------------------------------------
write_file_if_missing() {
  local target="$1"
  local content="$2"

  if [ -e "$target" ]; then
    echo "SKIP exists: $target"
    return
  fi

  mkdir -p "$(dirname "$target")"
  printf "%s\n" "$content" > "$target"
  echo "CREATED: $target"
}

# ==================================================
# MODULES PACKAGE
# ==================================================
write_file_if_missing "$BASE_DIR/app/modules/__init__.py" \
"# Domain modules package
"

# ==================================================
# USERS MODULE (NO MODELS HERE)
# ==================================================
write_file_if_missing "$BASE_DIR/app/modules/users/__init__.py" \
"# Users domain module
"

write_file_if_missing "$BASE_DIR/app/modules/users/routes.py" \
"from flask import Blueprint, jsonify
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
"

write_file_if_missing "$BASE_DIR/app/modules/users/services.py" \
"# Business logic for Users module.
# NO request / response objects here.

from app.models.auth import UserAccount

def list_users_service():
    users = UserAccount.query.limit(50).all()
    return [
        {
            'id': u.id,
            'email': u.email,
            'role_id': u.role_id,
            'is_active': u.is_active,
        }
        for u in users
    ]
"

write_file_if_missing "$BASE_DIR/app/modules/users/permissions.py" \
"# Users permissions.
# Keep role logic centralized here.
# TODO: fine-grained permissions later
"

write_file_if_missing "$BASE_DIR/app/modules/users/schemas.py" \
"# Users request/response schemas.
# Intentionally empty for now.
"

# ==================================================
# ACADEMICS MODULE (SKELETON ONLY)
# ==================================================
write_file_if_missing "$BASE_DIR/app/modules/academics/__init__.py" \
"# Academics domain module
"

write_file_if_missing "$BASE_DIR/app/modules/academics/routes.py" \
"from flask import Blueprint

academics_bp = Blueprint('academics', __name__)
# TODO: add routes
"

write_file_if_missing "$BASE_DIR/app/modules/academics/services.py" \
"# Academics business logic
"

write_file_if_missing "$BASE_DIR/app/modules/academics/permissions.py" \
"# Academics permissions
"

write_file_if_missing "$BASE_DIR/app/modules/academics/schemas.py" \
"# Academics schemas
"

# ==================================================
# FINANCE MODULE (SKELETON ONLY)
# ==================================================
write_file_if_missing "$BASE_DIR/app/modules/finance/__init__.py" \
"# Finance domain module
"

write_file_if_missing "$BASE_DIR/app/modules/finance/routes.py" \
"from flask import Blueprint

finance_bp = Blueprint('finance', __name__)
# TODO: add routes
"

write_file_if_missing "$BASE_DIR/app/modules/finance/services.py" \
"# Finance business logic
"

write_file_if_missing "$BASE_DIR/app/modules/finance/permissions.py" \
"# Finance permissions
"

write_file_if_missing "$BASE_DIR/app/modules/finance/schemas.py" \
"# Finance schemas
"

# ==================================================
# API V1 REGISTRY (FAIL FAST)
# ==================================================
write_file_if_missing "$BASE_DIR/app/api/__init__.py" \
"# API package
"

write_file_if_missing "$BASE_DIR/app/api/v1/__init__.py" \
"# API v1 package
"

write_file_if_missing "$BASE_DIR/app/api/v1/blueprint.py" \
"from flask import Blueprint

from app.modules.users.routes import users_bp
from app.modules.academics.routes import academics_bp
from app.modules.finance.routes import finance_bp

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api_v1.register_blueprint(users_bp, url_prefix='/users')
api_v1.register_blueprint(academics_bp, url_prefix='/academics')
api_v1.register_blueprint(finance_bp, url_prefix='/finance')
"

echo "Done. Module skeleton created safely."
