from flask import Blueprint, request, jsonify, current_app,g
from app.extensions import db
from app.middleware.role_decorators import require_roles,login_required
from app.modules.admin.services import admin_onboard_staff
admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/onboarding/staff", methods=["POST"])
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