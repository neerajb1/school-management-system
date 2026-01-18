# app/core/jwt_utils.py

import jwt
import uuid
from datetime import datetime, timedelta
from flask import current_app
from app.extensions import db
from app.models.auth import RevokedToken


ACCESS_TOKEN_TTL_MINUTES = 15
REFRESH_TOKEN_TTL_DAYS = 7


# ─────────────────────────────────────────────
# Access token
# ─────────────────────────────────────────────
def generate_access_token(user_id: int) -> str:
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(user_id),           # JWT spec: MUST be string
        "jti": jti,
        "type": "access",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TTL_MINUTES),
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )


# ─────────────────────────────────────────────
# Refresh token
# ─────────────────────────────────────────────
def generate_refresh_token(user_id: int) -> str:
    jti = str(uuid.uuid4())

    payload = {
        "sub": str(user_id),
        "jti": jti,
        "type": "refresh",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_TTL_DAYS),
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )


# ─────────────────────────────────────────────
# 🔒 Backward compatibility
# ─────────────────────────────────────────────
def generate_token(user_id: int) -> str:
    """
    DO NOT REMOVE until legacy callers are migrated.
    """
    return generate_access_token(user_id)


# ─────────────────────────────────────────────
# Decode token (authoritative)
# ─────────────────────────────────────────────
def decode_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        current_app.config["JWT_SECRET_KEY"],
        algorithms=["HS256"],
        options={"verify_exp": True},
    )

    # Only ACCESS tokens are revocable
    if payload.get("type") == "access":
        revoked = (
            db.session.query(RevokedToken)
            .filter_by(jti=payload["jti"])
            .first()
        )
        if revoked:
            raise jwt.InvalidTokenError("Token revoked")

    return payload


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def get_user_id_from_token(payload: dict) -> int:
    return int(payload["sub"])


def assert_access_token(payload: dict):
    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Access token required")


def assert_refresh_token(payload: dict):
    if payload.get("type") != "refresh":
        raise jwt.InvalidTokenError("Refresh token required")
