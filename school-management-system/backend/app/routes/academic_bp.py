from flask import Blueprint, jsonify, request
from app.models.academics import Subject, Attendance  # Updated import
from app import db

academic_bp = Blueprint('academic_bp', __name__)

@academic_bp.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([subject.to_dict() for subject in subjects]), 200

@academic_bp.route('/subjects', methods=['POST'])
def create_subject():
    data = request.get_json()
    try:
        subject = Subject(
            name=data['name'],
            code=data['code']
        )
        db.session.add(subject)
        db.session.commit()
        return jsonify({"message": "Subject created successfully", "subject_id": subject.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@academic_bp.route('/attendance', methods=['GET'])
def get_attendance():
    attendance_records = Attendance.query.all()
    return jsonify([record.to_dict() for record in attendance_records]), 200

@academic_bp.route('/attendance', methods=['POST'])
def create_attendance():
    data = request.get_json()
    try:
        attendance = Attendance(
            enrollment_id=data['enrollment_id'],
            attendance_date=data['attendance_date'],
            status=data['status'],
            attendance_remarks=data.get('attendance_remarks')
        )
        db.session.add(attendance)
        db.session.commit()
        return jsonify({"message": "Attendance record created successfully", "attendance_id": attendance.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
