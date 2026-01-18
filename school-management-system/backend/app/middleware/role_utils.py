# app/middleware/role_utils.py
from app.extensions import db
from app.models.users import UserAccount,Role


def get_current_user_role_name(user_id):
    result = (
        db.session.query(Role.name)
        .join(UserAccount, UserAccount.role_id == Role.id)
        .filter(UserAccount.id == user_id, UserAccount.is_active == True)
        .first()
    )

    return result[0] if result else None
