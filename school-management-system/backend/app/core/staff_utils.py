from datetime import datetime
from app.extensions import db
from app.models.users import Staff


def generate_emp_id() -> str:
    """
    Generates unique employee ID like:
    EMP-2026-0001
    """

    year = datetime.utcnow().year

    last_staff = (
        db.session.query(Staff)
        .order_by(Staff.id.desc())
        .first()
    )

    next_seq = (last_staff.id + 1) if last_staff else 1

    return f"EMP-{year}-{str(next_seq).zfill(4)}"
