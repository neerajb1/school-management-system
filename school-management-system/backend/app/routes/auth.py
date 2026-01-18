from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime
from app.extensions import db
from app.models.users import UserAccount
from app.models.auth import RevokedToken
from app.core.jwt_utils import generate_token, decode_token
from app.middleware.auth_decorators import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = (
        db.session.query(UserAccount)
        .filter_by(email=email, is_active=True)
        .first()
    )

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user.id)

    return jsonify({
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 86400
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ", 1)[1]

    payload = decode_token(token)

    revoked = RevokedToken(
        jti=payload["jti"],
        reason="logout",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.session.add(revoked)
    db.session.commit()

    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route("/verify", methods=["GET"])
def verify_token():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header missing"}), 401

    token = auth_header.split(" ", 1)[1]

    try:
        payload = decode_token(token)
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    user_id = int(payload["sub"])   # ✅ THIS WAS THE BUG

    user = (
        db.session.query(UserAccount)
        .filter_by(id=user_id, is_active=True)
        .first()
    )

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "valid": True,
        "user": {
            "id": user.id,
            "email": user.email,
            "role_id": user.role_id,
            "is_active": user.is_active,
        },
        "token": {
            "type": payload["type"],
            "expires_at": payload["exp"],
        }
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json(silent=True) or {}
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "refresh_token required"}), 400

    payload = decode_token(refresh_token)

    if payload["type"] != "refresh":
        return jsonify({"error": "Invalid token type"}), 401

    # Revoke old refresh token
    revoked = RevokedToken(
        jti=payload["jti"],
        reason="refresh_rotation",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.session.add(revoked)

    user_id = int(payload["sub"])

    from app.core.jwt_utils import generate_access_token, generate_refresh_token

    new_access = generate_access_token(user_id)
    new_refresh = generate_refresh_token(user_id)

    db.session.commit()

    return jsonify({
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "Bearer",
    }), 200
