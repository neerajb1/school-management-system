from app.core.audit_context import get_current_user_id
from app.models.users import UserAccount
from app.extensions import db


def get_current_user():
    user_id = get_current_user_id()
    if not user_id:
        return None

    return (
        db.session.query(UserAccount)
        .filter_by(id=user_id, is_active=True)
        .first()
    )
