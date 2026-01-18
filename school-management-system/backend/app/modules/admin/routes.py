from flask import Blueprint, request, jsonify, current_app,g
from app.extensions import db
from app.middleware.role_decorators import require_roles,login_required
from app.modules.admin.services import (admin_onboard_staff,
                                        admin_onboard_student,
                                        admin_onboard_parent,
                                        link_student_to_guardian                                       
                                        ,admin_unlink_student_parent)


# ─────────────────────────────────────────────

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/onboard/staff", methods=["POST"])
@login_required
def staff_onboarding():

    data = request.get_json(silent=True) or {}

    if not data.get("first_name"):
        return jsonify({
            "error": "first_name is required"
        }), 400

    try:
        staff = admin_onboard_staff(
        admin_user_id=g.current_user_id,
        data=data,
    )

        db.session.commit()

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Staff onboarding failed")
        return jsonify({
            "error": "Staff onboarding failed",
            "detail": str(e),
        }), 500

    return jsonify({
        "message": "Staff onboarded successfully",
        "staff": {
            "id": staff.id,
            "emp_id": staff.emp_id,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "department_id": staff.department_id,
        }
    }), 201


# ─────────────────────────────────────────────
# Student
# ─────────────────────────────────────────────
@admin_bp.route("/onboard/student", methods=["POST"])
@login_required
@require_roles("ADMIN")
def onboard_student():
    data = request.get_json(silent=True) or {}

    required = ["user_id", "first_name", "gender"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    try:
        student = admin_onboard_student(
            admin_user_id=g.current_user_id,
            data=data,
        )
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Student onboarding failed"}), 500

    return jsonify({
        "id": student.id,
        "admission_no": student.admission_no,
        "first_name": student.first_name,
    }), 201


# ─────────────────────────────────────────────
# Parent
# ─────────────────────────────────────────────
@admin_bp.route("/onboard/parent", methods=["POST"])
@login_required
@require_roles("ADMIN")
def onboard_parent():
    data = request.get_json(silent=True) or {}

    required = ["user_id", "emergency_contact"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    try:
        guardian = admin_onboard_parent(
            admin_user_id=g.current_user_id,
            data=data,
        )
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Parent onboarding failed"}), 500

    return jsonify({
        "id": guardian.id,
        "emergency_contact": guardian.emergency_contact,
    }), 201


@admin_bp.route("/guardian/link-student", methods=["POST"])
@login_required
@require_roles("ADMIN")
def link_student():
    data = request.get_json(silent=True) or {}

    guardian_id = data.get("guardian_id")
    student_id = data.get("student_id")

    if not guardian_id or not student_id:
        return jsonify({"error": "guardian_id and student_id required"}), 400

    try:
        student = link_student_to_guardian(
            admin_user_id=g.current_user_id,
            guardian_id=guardian_id,
            student_id=student_id,
        )
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 409
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Linking failed"}), 500

    return jsonify({
        "message": "Student linked to parent successfully",
        "student_id": student.id,
        "guardian_id": student.guardian_id,
    }), 201

@admin_bp.route("/student/unlink-parent", methods=["POST"])
@login_required
@require_roles("ADMIN")
def unlink_student_parent():
    data = request.get_json(silent=True) or {}

    student_id = data.get("student_id")
    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    try:
        student = admin_unlink_student_parent(
            admin_user_id=g.current_user_id,
            student_id=student_id,
        )

        db.session.commit()

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to unlink parent"}), 500

    return jsonify({
        "message": "Parent unlinked successfully",
        "student": {
            "id": student.id,
            "guardian_id": None
        }
    }), 200

