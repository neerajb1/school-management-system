from flask import Blueprint, jsonify, request
from app.models.academics import Attendance, Enrollment, ClassRoom  # Import Attendance, Enrollment, ClassRoom
from app.models.users import Student  # Import Student from app.models.users
from app.models.base import db

attendance_bp = Blueprint("attendance_bp", __name__)

@attendance_bp.route("/", methods=["GET"])
def get_attendance():
    # Get query parameters
    date = request.args.get("date")  # Optional date filter
    grade = request.args.get("grade")  # Optional grade filter
    section = request.args.get("section")  # Optional section filter

    # Build the base query
    query = (
        db.session.query(
            Attendance.id.label("attendanceId"),
            Attendance.attendance_date.label("date"),
            Attendance.status.label("status"),
            Attendance.attendance_remarks.label("remarks"),
            Enrollment.roll_no.label("rollNumber"),
            db.func.concat(Student.first_name, " ", Student.last_name).label("studentName"),
            ClassRoom.grade.label("grade"),
            ClassRoom.section.label("section"),
        )
        .join(Enrollment, Enrollment.id == Attendance.enrollment_id)
        .join(Student, Student.id == Enrollment.student_id)
        .join(ClassRoom, ClassRoom.id == Enrollment.class_id)
    )

    # Apply filters if provided
    if date:
        query = query.filter(Attendance.attendance_date == date)
    if grade:
        query = query.filter(ClassRoom.grade == grade)
    if section:
        query = query.filter(ClassRoom.section == section)

    # Execute the query and fetch results
    attendance_records = query.all()

    # Aggregate stats
    stats = {
        "present": sum(1 for record in attendance_records if record.status == "PRESENT"),
        "absent": sum(1 for record in attendance_records if record.status == "ABSENT"),
        "late": sum(1 for record in attendance_records if record.status == "LATE"),
    }

    # Format the response data
    records = [
        {
            "attendanceId": record.attendanceId,
            "date": record.date.isoformat(),
            "status": record.status,
            "remarks": record.remarks,
            "rollNumber": record.rollNumber,
            "studentName": record.studentName,
            "grade": record.grade,
            "section": record.section,
        }
        for record in attendance_records
    ]

    return jsonify({"stats": stats, "records": records}), 200
