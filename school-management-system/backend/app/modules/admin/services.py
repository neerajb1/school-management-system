from app.extensions import db
from app.models.users import UserAccount, Staff
from app.core.id_generators import generate_staff_emp_id
from flask import current_app

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
