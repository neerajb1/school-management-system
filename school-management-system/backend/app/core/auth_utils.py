from app.core.audit_context import get_current_user_id
from app.models.users import UserAccount
from app.extensions import db
from datetime import datetime
from app.models.refresh_token import RefreshToken
from app.models.users import UserAccount, Role
from werkzeug.security import generate_password_hash


def get_current_user():
    user_id = get_current_user_id()
    if not user_id:
        return None

    return (
        db.session.query(UserAccount)
        .filter_by(id=user_id, is_active=True)
        .first()
    )



def store_refresh_token(jti, user_id, expires_at):
    token = RefreshToken(
        jti=jti,
        user_id=user_id,
        expires_at=expires_at,
        is_revoked=False,
        created_by_id=user_id,
    )
    db.session.add(token)
    db.session.commit()


def revoke_refresh_token(jti, user_id):
    token = RefreshToken.query.filter_by(jti=jti).first()
    if token and not token.is_revoked:
        token.is_revoked = True
        token.updated_by_id = user_id
        db.session.commit()


def is_refresh_token_valid(jti):
    token = RefreshToken.query.filter_by(jti=jti).first()
    if not token:
        return False
    if token.is_revoked:
        return False
    if token.expires_at < datetime.utcnow():
        return False
    return True


def create_user_account(
    *,
    email: str,
    password: str,
    full_name: str,
    phone: str,
    user_type: str,
):
    role = (
        db.session.query(Role)
        .filter(Role.name == user_type)
        .one_or_none()
    )

    if not role:
        raise ValueError(f"Invalid user_type: {user_type}")

    user = UserAccount(
        email=email.lower().strip(),
        password_hash=generate_password_hash(password,method="pbkdf2:sha256",
    salt_length=16,),
        full_name=full_name.strip(),
        phone=phone,
        user_type=user_type,
        role_id=role.id,
        account_status="PENDING_ONBOARDING",
        is_active=False,
    )

    db.session.add(user)
    db.session.flush()  # get user.id safely

    return user