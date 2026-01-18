from flask import Blueprint, request, jsonify,g
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime
from app.extensions import db
from app.models.users import UserAccount
from app.models.auth import RevokedToken
from app.core.jwt_utils import generate_token, decode_token, get_user_id_from_token,generate_refresh_token
from app.middleware.auth_decorators import login_required
from app.core.auth_utils import (
    store_refresh_token,
    revoke_refresh_token,
    is_refresh_token_valid,
)
from app.models.refresh_token import RefreshToken
from sqlalchemy.exc import IntegrityError
from app.core.auth_utils import create_user_account
from app.modules.users.services import admin_onboard_staff


auth_bp = Blueprint("auth", __name__)
import inspect
from flask import current_app


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

    if not user or not user.is_active:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user.id)
    refresh_token = generate_refresh_token(user.id)
    refresh_payload = decode_token(refresh_token)
    store_refresh_token(
        jti=refresh_payload["jti"],
        user_id=user.id,
        expires_at=datetime.utcfromtimestamp(refresh_payload["exp"]),
    )

    return jsonify({
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": 86400
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    auth_header = request.headers.get("Authorization")
    if not auth_header.startswith("Bearer "):
        return "", 204
    token = auth_header.split(" ", 1)[1]

    try:
        payload = decode_token(token)
    except Exception:
        return "", 204
    
    jti = payload.get("jti")
    user_id = get_user_id_from_token(payload)
    if jti:

        revoked = RevokedToken(
            jti=payload["jti"],
            reason="logout",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add(revoked)
        db.session.commit()

        revoke_refresh_token(jti, user_id)
        return jsonify({"message": "Logged out successfully"}), 200
    return "", 204

    


@auth_bp.route("/verify", methods=["GET"])
def verify_token():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header missing"}), 401

    token = auth_header.split(" ", 1)[1]

    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError as e:
        return jsonify({"error": "Token expired", "detail": str(e)}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": "Invalid token", "detail": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Unexpected error", "detail": str(e)}), 500

    if payload.get("type") != "access":
        return jsonify({"error": "Invalid token type"}), 401

    user_id = get_user_id_from_token(payload)

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
    
    if refresh_token.startswith("Bearer "):
        refresh_token = refresh_token[len("Bearer "):]

    try:
        payload = decode_token(refresh_token)
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


    if payload.get("type") != "refresh":
        return jsonify({"error": "Invalid token type"}), 401

    user_id = get_user_id_from_token(payload)
    jti = payload["jti"]

    if not is_refresh_token_valid(jti):
        return jsonify({"error": "Refresh token revoked"}), 403

    # Rotate token
    revoke_refresh_token(jti, user_id)

    new_access = generate_token(user_id)
    new_refresh = generate_refresh_token(user_id)

    new_payload = decode_token(new_refresh)

    store_refresh_token(
        jti=new_payload["jti"],
        user_id=user_id,
        expires_at=datetime.utcfromtimestamp(new_payload["exp"]),
    )

    return jsonify(
        {
            "access_token": new_access,
            "refresh_token": new_refresh,
        }
    ), 200


@auth_bp.route("/logout-all", methods=["POST"])
@login_required
def logout_all_sessions():
    """
    Logout user from ALL sessions (all devices).
    """

    user_id = g.current_user_id

    # 1️⃣ Revoke ALL refresh tokens for this user
    (
        db.session.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked.is_(False),
        )
        .update(
            {
                RefreshToken.is_revoked: True,
                RefreshToken.updated_by_id: user_id,
            },
            synchronize_session=False,
        )
    )

    # 2️⃣ Revoke current access token immediately
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_token(token)
            jti = payload.get("jti")
            if jti:
                db.session.add(
                    RevokedToken(
                        jti=jti,
                        created_by_id=user_id,
                    )
                )
        except Exception:
            # Token already invalid → nothing to do
            pass

    db.session.commit()

    return "", 204

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    required_fields = ["email", "password", "full_name", "user_type"]
    missing = [f for f in required_fields if not data.get(f)]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    try:
        user = create_user_account(
            email=data["email"],
            password=data["password"],
            full_name=data["full_name"],
            phone=data.get("phone"),
            user_type=data["user_type"].upper(),
        )

        db.session.commit()

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409

    access_token = generate_token(user.id)
    refresh_token = generate_refresh_token(user.id)

    return jsonify({
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "user_type": user.user_type,
            "account_status": user.account_status,
        },
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }
    }), 201



@auth_bp.route("/onboarding/staff", methods=["POST"])
@login_required
def staff_onboarding():
#     current_app.logger.error(
#     "ONBOARD DEBUG  status=%s",
#     g.current_account_status
# )
#     if g.current_account_status != "PENDING_ONBOARDING":
#         return jsonify({
#             "error": "Account already onboarded"
#         }), 403

    data = request.get_json(silent=True) or {}

    if not data.get("first_name"):
        return jsonify({
            "error": "first_name is required"
        }), 400

    try:
        staff = admin_onboard_staff(
        admin_user_id=g.current_user_id,
        data=data,
    )

        db.session.commit()

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Staff onboarding failed")
        return jsonify({
            "error": "Staff onboarding failed",
            "detail": str(e),
        }), 500

    return jsonify({
        "message": "Staff onboarded successfully",
        "staff": {
            "id": staff.id,
            "emp_id": staff.emp_id,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "department_id": staff.department_id,
        }
    }), 201

