from flask import Blueprint, jsonify, request
from app.models.academics import Subject, ClassRoom  # Updated import
from app import db

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Subject.query.all()
    return jsonify([course.to_dict() for course in courses]), 200

@course_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    try:
        course = Subject(
            name=data['name'],
            code=data['code']
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({"message": "Course created successfully", "course_id": course.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@course_bp.route('/classes', methods=['GET'])
def get_classes():
    classes = ClassRoom.query.all()
    return jsonify([class_room.to_dict() for class_room in classes]), 200

@course_bp.route('/classes', methods=['POST'])
def create_class():
    data = request.get_json()
    try:
        class_room = ClassRoom(
            grade=data['grade'],
            section=data['section']
        )
        db.session.add(class_room)
        db.session.commit()
        return jsonify({"message": "Class created successfully", "class_id": class_room.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400