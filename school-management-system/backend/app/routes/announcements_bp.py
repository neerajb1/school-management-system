from flask import Blueprint, jsonify, request

announcements_bp = Blueprint('announcements_bp', __name__)

# Example route to get all announcements
@announcements_bp.route('/', methods=['GET'])
def get_announcements():
    # Replace this with actual database logic
    announcements = [
        {"id": 1, "title": "Holiday Notice", "content": "School will remain closed on 25th December."},
        {"id": 2, "title": "Exam Schedule", "content": "The final exams will start from 1st March."}
    ]
    return jsonify(announcements), 200

# Example route to create an announcement
@announcements_bp.route('/', methods=['POST'])
def create_announcement():
    data = request.get_json()
    # Replace this with actual database logic
    new_announcement = {
        "id": 3,  # This should be generated dynamically
        "title": data.get("title"),
        "content": data.get("content")
    }
    return jsonify({"message": "Announcement created successfully", "announcement": new_announcement}), 201
