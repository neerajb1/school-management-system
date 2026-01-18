from app.core.audit_context import get_current_user_id
from app.models.users import UserAccount
from app.extensions import db
from datetime import datetime
from app.models.refresh_token import RefreshToken
from app.models.users import UserAccount, Role
from werkzeug.security import generate_password_hash
import logging

logger = logging.getLogger(__name__)

def get_current_user():
    user_id = get_current_user_id()
    if not user_id:
        logger.warning("No current user found")
        return None

    user = (
        db.session.query(UserAccount)
        .filter_by(id=user_id, is_active=True)
        .first()
    )
    if user:
        logger.info("Current user retrieved", extra={"user_id": user.id})
    else:
        logger.warning("Current user not found or inactive", extra={"user_id": user_id})
    return user

def store_refresh_token(jti, user_id, expires_at):
    logger.info("Storing refresh token", extra={"user_id": user_id, "jti": jti})
    token = RefreshToken(
        jti=jti,
        user_id=user_id,
        expires_at=expires_at,
        is_revoked=False,
        created_by_id=user_id,
    )
    db.session.add(token)
    db.session.commit()
    logger.info("Refresh token stored successfully", extra={"user_id": user_id, "jti": jti})

def revoke_refresh_token(jti, user_id):
    logger.info("Revoking refresh token", extra={"user_id": user_id, "jti": jti})
    token = RefreshToken.query.filter_by(jti=jti).first()
    if token and not token.is_revoked:
        token.is_revoked = True
        token.updated_by_id = user_id
        db.session.commit()
        logger.info("Refresh token revoked", extra={"user_id": user_id, "jti": jti})
    else:
        logger.warning("Refresh token not found or already revoked", extra={"jti": jti})

def is_refresh_token_valid(jti):
    token = RefreshToken.query.filter_by(jti=jti).first()
    if not token:
        logger.warning("Refresh token not found", extra={"jti": jti})
        return False
    if token.is_revoked:
        logger.warning("Refresh token is revoked", extra={"jti": jti})
        return False
    if token.expires_at < datetime.utcnow():
        logger.warning("Refresh token is expired", extra={"jti": jti})
        return False
    logger.info("Refresh token is valid", extra={"jti": jti})
    return True

def create_user_account(
    *,
    email: str,
    password: str,
    full_name: str,
    phone: str,
    user_type: str,
):
    logger.info("Creating user account", extra={"email": email, "user_type": user_type})
    role = (
        db.session.query(Role)
        .filter(Role.name == user_type)
        .one_or_none()
    )

    if not role:
        logger.warning("Invalid user_type provided", extra={"user_type": user_type})
        raise ValueError(f"Invalid user_type: {user_type}")

    user = UserAccount(
        email=email.lower().strip(),
        password_hash=generate_password_hash(password, method="pbkdf2:sha256", salt_length=16),
        full_name=full_name.strip(),
        phone=phone,
        user_type=user_type,
        role_id=role.id,
        account_status="PENDING_ONBOARDING",
        is_active=False,
    )

    db.session.add(user)
    db.session.flush()  # get user.id safely
    logger.info("User account created", extra={"user_id": user.id, "email": email})
    return user