from flask import Blueprint, jsonify, request
from app.models.users import Staff  # Updated import
from app.models.academics import TeacherAssignment
from app import db

teacher_bp = Blueprint('teacher_bp', __name__)

@teacher_bp.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Staff.query.all()
    return jsonify([teacher.to_dict() for teacher in teachers]), 200

@teacher_bp.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    teacher = Staff.query.get(teacher_id)
    if not teacher:
        return jsonify({"error": "Teacher not found"}), 404
    return jsonify(teacher.to_dict()), 200

@teacher_bp.route('/teachers', methods=['POST'])
def create_teacher():
    data = request.get_json()
    try:
        teacher = Staff(
            emp_id=data['emp_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            role_id=data['role_id'],
            department_id=data['department_id']
        )
        db.session.add(teacher)
        db.session.commit()
        return jsonify({"message": "Teacher created successfully", "teacher_id": teacher.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400