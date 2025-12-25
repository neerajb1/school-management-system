from flask import Blueprint, jsonify, request
from app.models.users import Student, Guardian
from app.models.academics import Enrollment, ClassRoom, Subject, Attendance, Marksheet
from app.models.base import db

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/', methods=['GET'])
def get_students():
    # Query to join multiple tables and fetch required fields
    students = (
        db.session.query(
            Student.id,
            Student.admission_no.label("admissionId"),
            Enrollment.roll_no.label("rollNumber"),
            db.func.concat(Student.first_name, " ", Student.last_name).label("name"),
            Student.gender,
            Student.dob,
            Student.email,
            Student.phone.label("contact"),
            Student.photo_url.label("address"),
            ClassRoom.grade,
            ClassRoom.section,
            Student.admission_date,
            Guardian.father_name,
            Guardian.father_occupation,
            Guardian.mother_name,
            Guardian.parent_email,
            Guardian.emergency_contact,
            Enrollment.status,
        )
        .join(Enrollment, Enrollment.student_id == Student.id)
        .join(ClassRoom, ClassRoom.id == Enrollment.class_id)
        .join(Guardian, Guardian.id == Student.guardian_id)
        .all()
    )

    # Restructure the data into the required format
    students_data = [
        {
            "id": student.id,
            "admissionId": student.admissionId,
            "rollNumber": student.rollNumber,
            "name": student.name,
            "gender": student.gender.value if student.gender else None,
            "dob": student.dob.isoformat() if student.dob else None,
            "bloodGroup": None,  # Assuming bloodGroup is not available
            "email": student.email,
            "contact": student.contact,
            "address": student.address,
            "grade": f"Grade {student.grade}",
            "section": student.section,
            "admissionDate": student.admission_date.isoformat() if student.admission_date else None,
            "fatherName": student.father_name,
            "fatherOccupation": student.father_occupation,
            "motherName": student.mother_name,
            "parentEmail": student.parent_email,
            "emergencyContact": student.emergency_contact,
            "status": student.status,
            "transport": None,  # Assuming transport is not available
            "busRoute": None,  # Explicitly set busRoute to null
            "medicalConditions": None,  # Assuming medicalConditions is not available
        }
        for student in students
    ]

    return jsonify(students_data), 200

@student_bp.route('/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = (
        db.session.query(
            Student.id,
            Student.admission_no.label("admissionId"),
            db.func.concat(Student.first_name, " ", Student.last_name).label("name"),
            Student.gender,
            Student.dob,
            Student.email,
            Student.phone.label("contact"),
            Student.photo_url.label("address"),
            ClassRoom.grade,
            ClassRoom.section,
            Guardian.father_name.label("fatherName"),
            Guardian.mother_name.label("motherName"),
            Guardian.emergency_contact.label("emergencyContact"),
        )
        .join(Enrollment, Enrollment.student_id == Student.id)
        .join(ClassRoom, ClassRoom.id == Enrollment.class_id)
        .join(Guardian, Guardian.id == Student.guardian_id)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        return jsonify({"error": "Student not found"}), 404

    student_data = {
        "id": student.id,
        "admissionId": student.admissionId,
        "name": student.name,
        "gender": student.gender.value if student.gender else None,
        "dob": student.dob.isoformat() if student.dob else None,
        "email": student.email,
        "contact": student.contact,
        "address": student.address,
        "grade": f"Grade {student.grade}",
        "section": student.section,
        "fatherName": student.fatherName,
        "motherName": student.motherName,
        "emergencyContact": student.emergencyContact,
    }

    return jsonify(student_data), 200

@student_bp.route('/', methods=['POST'])
def create_student():
    data = request.get_json()
    try:
        student = Student(
            admission_no=data['admission_no'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=data['dob'],
            gender=data['gender'],
            nationality=data['nationality'],
            email=data['email'],
            phone=data['phone'],
            photo_url=data.get('photo_url'),
            admission_date=data['admission_date']
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Student created successfully", "student_id": student.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@student_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    try:
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        student.phone = data.get('phone', student.phone)
        db.session.commit()
        return jsonify({"message": "Student updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@student_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@student_bp.route('/<int:student_id>/results', methods=['GET'])
def get_student_results(student_id):
    results = (
        db.session.query(
            Subject.name.label("subject"),
            Marksheet.marks_obtained.label("marksObtained"),
            Marksheet.total_marks.label("totalMarks"),
        )
        .join(Marksheet, Marksheet.subject_id == Subject.id)
        .join(Enrollment, Enrollment.id == Marksheet.enrollment_id)
        .filter(Enrollment.student_id == student_id)
        .all()
    )

    if not results:
        return jsonify({"results": []}), 200

    results_data = [
        {
            "subject": result.subject,
            "marksObtained": result.marksObtained,
            "totalMarks": result.totalMarks,
        }
        for result in results
    ]

    return jsonify({"results": results_data}), 200

@student_bp.route('/<int:student_id>/attendance', methods=['GET'])
def get_student_attendance(student_id):
    attendance_records = (
        db.session.query(
            db.func.count(Attendance.id).label("total"),
            db.func.sum(
                db.case(
                    (Attendance.status == "PRESENT", 1),
                    else_=0
                )
            ).label("present"),
        )
        .join(Enrollment, Enrollment.id == Attendance.enrollment_id)
        .filter(Enrollment.student_id == student_id)
        .first()
    )

    if not attendance_records or attendance_records.total == 0:
        return jsonify({"attendancePercentage": 0}), 200

    attendance_percentage = (attendance_records.present / attendance_records.total) * 100
    return jsonify({"attendancePercentage": round(attendance_percentage, 2)}), 200

@student_bp.route('/attendance', methods=['GET'])
def get_attendance():
    # Get query parameters
    date = request.args.get('date')  # Optional date filter
    grade = request.args.get('grade')  # Optional grade filter
    section = request.args.get('section')  # Optional section filter

    # Build the base query
    query = (
        db.session.query(
            Attendance.id.label("attendanceId"),
            Attendance.attendance_date.label("date"),
            Attendance.status.label("status"),
            Attendance.attendance_remarks.label("remarks"),
            Enrollment.roll_no.label("rollNumber"),
            db.func.concat(Student.first_name, " ", Student.last_name).label("studentName"),  # Use the Student model
            ClassRoom.grade.label("grade"),
            ClassRoom.section.label("section"),
        )
        .join(Enrollment, Enrollment.id == Attendance.enrollment_id)
        .join(Student, Student.id == Enrollment.student_id)  # Join with the Student model
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