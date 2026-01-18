from flask import request, jsonify,g
from app.extensions import db
from app.middleware.role_decorators import require_roles,login_required
from app.modules.admin.masters.services.class_service import create_class_service
from app.modules.admin.routes import admin_bp
from app.modules.admin.masters.services.subject_service import create_subject_service
from app.modules.admin.masters.services.academic_session_service import (
    create_academic_session_service,
)
from app.modules.admin.masters.services.fee_type_service import create_fee_type_service
from app.modules.admin.masters.services.grade_scale_service import (
    create_grade_scale_service,
)


# ─────────────────────────────────────────────
# CLASSES
# ─────────────────────────────────────────────


@admin_bp.route("/masters/classes", methods=["POST"])
@require_roles("ADMIN")
def create_class():
    data = request.get_json(silent=True) or {}

    try:
        cls = create_class_service(
            admin_user_id=g.current_user_id,
            data=data,
        )
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({"id": cls.id}), 201



@admin_bp.route("/masters/classes", methods=["GET"])
@login_required
@require_roles("ADMIN")
def list_classes():
    from app.models.academics import ClassRoom

    classes = ClassRoom.query.order_by(ClassRoom.id).all()

    response = jsonify([
        {
            "id": c.id,
            "name": c.name,
            "section": c.section,
        }
        for c in classes
    ])

    response.headers["Cache-Control"] = "public, max-age=3600"
    return response, 200


# ─────────────────────────────────────────────
# SUBJECTS
# ─────────────────────────────────────────────
@admin_bp.route("/masters/subjects", methods=["POST"])
@login_required
@require_roles("ADMIN")
def create_subject():
    data = request.get_json(silent=True) or {}

    try:
        subject = create_subject_service(
            admin_user_id=g.current_user_id,
            data=data,
        )
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Subject creation failed"}), 500

    return jsonify({
        "id": subject.id,
        "name": subject.name,
        "code": subject.code,
    }), 201

@admin_bp.route("/masters/subjects", methods=["GET"])
@login_required
@require_roles("ADMIN")
def list_subjects():
    from app.models.academics import Subject

    subjects = Subject.query.order_by(Subject.name).all()

    response = jsonify([
        {
            "id": s.id,
            "name": s.name,
            "code": s.code,
        }
        for s in subjects
    ])

    response.headers["Cache-Control"] = "public, max-age=3600"
    return response, 200

# ─────────────────────────────────────────────
# ACADEMIC SESSIONS
# ─────────────────────────────────────────────
@admin_bp.route("/masters/academic-sessions", methods=["POST"])
@login_required
@require_roles("ADMIN")
def create_academic_session():
    data = request.get_json(silent=True) or {}

    try:
        session = create_academic_session_service(
            admin_user_id=g.current_user_id,
            data=data,
        )
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Academic session creation failed"}), 500

    return jsonify({
        "id": session.id,
        "name": session.name,
        "is_active": session.is_active,
    }), 201

@admin_bp.route("/masters/academic-sessions", methods=["GET"])
@login_required
@require_roles("ADMIN")
def list_academic_sessions():
    from app.models.academics import AcademicSession

    sessions = AcademicSession.query.order_by(
        AcademicSession.start_date.desc()
    ).all()

    response = jsonify([
        {
            "id": s.id,
            "name": s.name,
            "start_date": s.start_date.isoformat() if s.start_date else None,
            "end_date": s.end_date.isoformat() if s.end_date else None,
            "is_active": s.is_active,
        }
        for s in sessions
    ])

    response.headers["Cache-Control"] = "public, max-age=1800"
    return response, 200


# ─────────────────────────────────────────────
# FEE TYPES
# ─────────────────────────────────────────────
@admin_bp.route("/masters/fee-types", methods=["POST"])
@login_required
@require_roles("ADMIN")
def create_fee_type():
    data = request.get_json(silent=True) or {}

    try:
        fee_type = create_fee_type_service(
            admin_user_id=g.current_user_id,
            data=data,
        )
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Fee type creation failed"}), 500

    return jsonify({
        "id": fee_type.id,
        "name": fee_type.name,
        "frequency": fee_type.frequency,
    }), 201


@admin_bp.route("/masters/fee-types", methods=["GET"])
@login_required
@require_roles("ADMIN")
def list_fee_types():
    from app.models.finance import FeeType

    fee_types = FeeType.query.order_by(FeeType.name).all()

    response = jsonify([
        {
            "id": f.id,
            "name": f.name,
            "frequency": f.frequency,
        }
        for f in fee_types
    ])

    response.headers["Cache-Control"] = "public, max-age=3600"
    return response, 200


# ─────────────────────────────────────────────
# GRADE SCALES
# ─────────────────────────────────────────────
@admin_bp.route("/masters/grade-scales", methods=["POST"])
@login_required
@require_roles("ADMIN")
def create_grade_scale():
    data = request.get_json(silent=True) or {}

    try:
        grade = create_grade_scale_service(
            admin_user_id=g.current_user_id,
            data=data,
        )
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Grade scale creation failed"}), 500

    return jsonify({
        "id": grade.id,
        "grade_name": grade.grade_name,
        "min_percentage": grade.min_percentage,
        "max_percentage": grade.max_percentage,
    }), 201

@admin_bp.route("/masters/grade-scales", methods=["GET"])
@login_required
@require_roles("ADMIN")
def list_grade_scales():
    from app.models.academics import GradeScale

    grades = GradeScale.query.order_by(GradeScale.min_percentage).all()

    response = jsonify([
        {
            "id": g.id,
            "grade_name": g.grade_name,
            "min_percentage": g.min_percentage,
            "max_percentage": g.max_percentage,
            "grade_point": g.grade_point,
        }
        for g in grades
    ])

    response.headers["Cache-Control"] = "public, max-age=3600"
    return response, 200
