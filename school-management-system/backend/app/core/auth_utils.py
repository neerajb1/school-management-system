from app.core.audit_context import get_current_user_id
from app.models.users import UserAccount
from app.extensions import db
from datetime import datetime
from app.models.refresh_token import RefreshToken



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