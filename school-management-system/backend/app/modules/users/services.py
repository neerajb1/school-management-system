# Business logic for Users module.
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

