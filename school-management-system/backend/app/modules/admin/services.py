from app.extensions import db
from app.core.id_generators import generate_staff_emp_id, generate_student_admission_no
from flask import current_app
from sqlalchemy import text

from app.models.users import (
    UserAccount,
    Staff,
    Student,
    Guardian
)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def _require_pending(user: UserAccount):
    if user.account_status != "PENDING_ONBOARDING":
        raise ValueError("Account already onboarded")


def _get_user_or_fail(user_id: int, expected_type: str) -> UserAccount:
    user = db.session.query(UserAccount).filter_by(id=user_id).first()
    if not user:
        raise ValueError("User not found")

    if user.user_type != expected_type:
        raise ValueError(f"Invalid user_type for {expected_type} onboarding")

    _require_pending(user)
    return user



# ─────────────────────────────────────────────
# Staff onboarding (ADMIN)
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# Student onboarding (ADMIN)
# ─────────────────────────────────────────────
def admin_onboard_student(admin_user_id: int, data: dict) -> Student:
    user = _get_user_or_fail(data["user_id"], "STUDENT")

    student = Student(
        user_account_id=user.id,
        admission_no=generate_student_admission_no(),
        first_name=data["first_name"],
        last_name=data.get("last_name"),
        dob=data.get("dob"),
        gender=data["gender"],
        nationality=data.get("nationality"),
        admission_date=data.get("admission_date"),
        created_by_id=admin_user_id,
        updated_by_id=admin_user_id,
    )

    db.session.add(student)

    user.account_status = "ACTIVE"

    return student

# ─────────────────────────────────────────────
# Parent onboarding (ADMIN)
# ─────────────────────────────────────────────
def admin_onboard_parent(admin_user_id: int, data: dict) -> Guardian:
    user = _get_user_or_fail(data["user_id"], "PARENT")

    guardian = Guardian(
        user_account_id=user.id,
        father_name=data.get("father_name"),
        mother_name=data.get("mother_name"),
        parent_email=user.email,
        emergency_contact=data["emergency_contact"],
        created_by_id=admin_user_id,
        updated_by_id=admin_user_id,
    )

    db.session.add(guardian)

    user.account_status = "ACTIVE"

    return guardian

def link_student_to_guardian(admin_user_id: int, guardian_id: int, student_id: int):
    guardian = db.session.query(Guardian).filter_by(id=guardian_id).first()
    if not guardian:
        raise ValueError("Guardian not found")

    student = db.session.query(Student).filter_by(id=student_id).first()
    if not student:
        raise ValueError("Student not found")

    if student.guardian_id:
        raise ValueError("Student already linked to a guardian")

    student.guardian_id = guardian.id
    student.updated_by_id = admin_user_id

    return student


def admin_unlink_student_parent(*, admin_user_id: int, student_id: int) -> Student:
    student = (
        db.session.query(Student)
        .filter_by(id=student_id)
        .first()
    )

    if not student:
        raise ValueError("Student not found")

    if not student.guardian_id:
        raise ValueError("Student is not linked to any guardian")

    # Unlink
    student.guardian_id = None
    student.updated_by_id = admin_user_id

    return student
