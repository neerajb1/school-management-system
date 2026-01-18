from typing import Dict, Any, List
from app.extensions import db
from datetime import datetime
from app.core.staff_utils import generate_emp_id
from app.core.crud_base import CRUDBase
from app.models.users import UserAccount, Staff
from app.middleware.role_utils import user_has_role
from app.core.exceptions import (
    PermissionDenied,
    NotFound,
    ValidationError,
)
from flask import current_app
from app.core.id_generators import generate_staff_emp_id

class UserService:
    def __init__(self):
        self.crud = CRUDBase(UserAccount)

    def list_users(self, *, current_user_id: int) -> List[Dict[str, Any]]:
        if not user_has_role(current_user_id, "ADMIN"):
            raise PermissionDenied("Not allowed to list users")

        users = self.crud.list(limit=100)
        return [self._serialize(u) for u in users]

    def get_user(self, *, user_id: int, current_user_id: int) -> Dict[str, Any]:
        if user_id != current_user_id and not user_has_role(current_user_id, "ADMIN"):
            raise PermissionDenied("Not allowed to view this user")

        user = self.crud.get_by_id(user_id)
        if not user:
            raise NotFound("User not found")

        return self._serialize(user)

    def create_user(self, *, data: Dict[str, Any], current_user_id: int) -> Dict[str, Any]:
        if not user_has_role(current_user_id, "ADMIN"):
            raise PermissionDenied("Not allowed to create users")

        allowed_fields = {"email", "role_id", "is_active"}
        payload = {k: v for k, v in data.items() if k in allowed_fields}

        if "email" not in payload or "role_id" not in payload:
            raise ValidationError("email and role_id are required")

        user = self.crud.create(payload)
        return self._serialize(user)

    def update_user(self, *, user_id: int, data: Dict[str, Any], current_user_id: int) -> Dict[str, Any]:
        if not user_has_role(current_user_id, "ADMIN"):
            raise PermissionDenied("Not allowed to update users")

        user = self.crud.get_by_id(user_id)
        if not user:
            raise NotFound("User not found")

        allowed_fields = {"email", "role_id", "is_active"}
        payload = {k: v for k, v in data.items() if k in allowed_fields}

        return self._serialize(self.crud.update(user, payload))

    def deactivate_user(self, *, user_id: int, current_user_id: int):
        if not user_has_role(current_user_id, "ADMIN"):
            raise PermissionDenied("Not allowed to deactivate users")

        user = self.crud.get_by_id(user_id)
        if not user:
            raise NotFound("User not found")

        self.crud.update(user, {"is_active": False})

    def _serialize(self, user: UserAccount) -> Dict[str, Any]:
        return {
            "id": user.id,
            "email": user.email,
            "role_id": user.role_id,
            "is_active": user.is_active,
        }


def admin_onboard_staff(*, admin_user_id: int, data: dict):
    user = (
    db.session.query(UserAccount)
    .filter_by(id=data["user_id"])
    .first()
)
    current_app.logger.error(
    "ONBOARD DEBUG user_id=%s status=%s is_active=%s",
    user.id,
    user.account_status,
    user.is_active,
)
    if not user:
        raise ValueError("User not found")

    if user.account_status != "PENDING_ONBOARDING":
        raise ValueError("User already onboarded")

    if user.user_type != "TEACHER":
        raise ValueError("User type mismatch")

    staff = Staff(
        user_account_id=user.id,
        first_name=data["first_name"],
        last_name=data.get("last_name"),
        joining_date=data.get("joining_date"),
        qualification=data.get("qualification"),
        department_id=data["department_id"],
        role_id=data["role_id"],
        photo_url=data.get("photo_url"),
        emp_id=generate_staff_emp_id(),
    )

    user.account_status = "ACTIVE"
    user.is_active = True

    db.session.add(staff)
    db.session.commit()

    return staff
