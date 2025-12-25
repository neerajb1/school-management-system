from flask import Blueprint, jsonify
from app.models.academics import Enrollment, Attendance
from app.models.users import Student
from sqlalchemy.sql import func
from app.models.base import db

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard_data():
    # Total Students
    total_students = db.session.query(func.count(Student.id)).scalar()

    # Active Students
    active_students = db.session.query(func.count(Enrollment.id)).filter(Enrollment.status == "Active").scalar()

    # New Admissions (e.g., students admitted in the last 30 days)
    new_admissions = db.session.query(func.count(Student.id)).filter(
        Student.admission_date >= func.date(func.now(), "-30 days")
    ).scalar()

    # Attendance Today
    attendance_today = db.session.query(func.count(Attendance.id)).filter(
        Attendance.attendance_date == func.current_date(),
        Attendance.status == "PRESENT"
    ).scalar()

    # Construct the response
    response = {
        "stats": {
            "summary": {
                "totalStudents": total_students or 0,
                "activeStudents": active_students or 0,
                "newAdmissions": new_admissions or 0,
            }
        },
        "attendanceToday": attendance_today or 0
    }

    return jsonify(response), 200
