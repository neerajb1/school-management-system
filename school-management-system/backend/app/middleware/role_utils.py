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

def user_has_role(user_id: int, role_name: str) -> bool:
    """
    Check whether a user has the given role.

    - DB is the source of truth
    - No caching here (can be added later)
    - Safe for services and decorators
    """
    result = (
        db.session.query(Role.name)
        .join(UserAccount, UserAccount.role_id == Role.id)
        .filter(UserAccount.id == user_id)
        .first()
    )

    if not result:
        return False

    return result[0] == role_name
