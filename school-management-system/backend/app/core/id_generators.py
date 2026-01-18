from app.extensions import db
from sqlalchemy import text

def generate_staff_emp_id() -> str:
    """
    Generates a unique staff employee ID.
    Format: EMP-<sequential number>
    """

    result = db.session.execute(
        text("SELECT nextval('staff_emp_id_seq')")
    ).scalar_one()

    return f"EMP-{result:06d}"

def generate_student_admission_no() -> str:
    result = db.session.execute(
        text("SELECT nextval('student_admission_seq')")
    ).scalar_one()

    return f"ADM-{result:06d}"
