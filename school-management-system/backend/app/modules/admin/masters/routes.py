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

@admin_bp.route("/masters/classes/<int:class_id>", methods=["GET"])
@login_required
@require_roles("ADMIN")
def get_class(class_id):
    from app.models.academics import ClassRoom

    cls = ClassRoom.query.get(class_id)
    if not cls:
        return jsonify({"error": "Class not found"}), 404

    return jsonify({
        "id": cls.id,
        "name": cls.name,
        "section": cls.section,
    }), 200

@admin_bp.route("/masters/classes/<int:class_id>", methods=["PUT"])
@login_required
@require_roles("ADMIN")
def update_class(class_id):
    from app.models.academics import ClassRoom, Enrollment

    cls = ClassRoom.query.get(class_id)
    if not cls:
        return jsonify({"error": "Class not found"}), 404

    # 🔒 Restriction: class already in use
    in_use = (
        db.session.query(Enrollment.id)
        .filter_by(class_id=class_id)
        .first()
    )
    if in_use:
        return jsonify({
            "error": "Class already in use and cannot be modified"
        }), 409

    data = request.get_json(silent=True) or {}

    if "name" in data:
        cls.name = data["name"]
    if "section" in data:
        cls.section = data["section"]

    db.session.commit()

    return jsonify({"message": "Class updated"}), 200

@admin_bp.route("/masters/classes/<int:class_id>", methods=["DELETE"])
@login_required
@require_roles("ADMIN")
def delete_class(class_id):
    from app.models.academics import ClassRoom, Enrollment

    cls = ClassRoom.query.get(class_id)
    if not cls:
        return jsonify({"error": "Class not found"}), 404

    if Enrollment.query.filter_by(class_id=class_id).first():
        return jsonify({
            "error": "Class already in use and cannot be deleted"
        }), 409

    db.session.delete(cls)
    db.session.commit()
    return jsonify({"message": "Class deleted"}), 200




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

@admin_bp.route("/masters/subjects/<int:subject_id>", methods=["DELETE"])
@login_required
@require_roles("ADMIN")
def delete_subject(subject_id):
    from app.models.academics import Subject, TeacherAssignment

    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    # 🔒 Check usage
    in_use = (
        db.session.query(TeacherAssignment.id)
        .filter_by(subject_id=subject_id)
        .first()
    )
    if in_use:
        return jsonify({
            "error": "Subject is already assigned and cannot be deleted"
        }), 409

    db.session.delete(subject)
    db.session.commit()

    return jsonify({"message": "Subject deleted"}), 200

@admin_bp.route("/masters/subjects/<int:subject_id>", methods=["PUT"])
@login_required
@require_roles("ADMIN")
def update_subject(subject_id):
    from app.models.academics import Subject, TeacherAssignment

    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    if TeacherAssignment.query.filter_by(subject_id=subject_id).first():
        return jsonify({
            "error": "Subject already in use and cannot be modified"
        }), 409

    data = request.get_json(silent=True) or {}

    if "name" in data:
        subject.name = data["name"]
    if "code" in data:
        subject.code = data["code"]

    db.session.commit()
    return jsonify({"message": "Subject updated"}), 200


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

@admin_bp.route("/masters/academic-sessions/<int:session_id>", methods=["GET"])
@login_required
@require_roles("ADMIN")
def get_academic_session(session_id):
    from app.models.academics import AcademicSession

    session = AcademicSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Academic session not found"}), 404

    return jsonify({
        "id": session.id,
        "name": session.name,
        "start_date": session.start_date.isoformat() if session.start_date else None,
        "end_date": session.end_date.isoformat() if session.end_date else None,
        "is_active": session.is_active,
    }), 200

@admin_bp.route("/masters/academic-sessions/<int:session_id>", methods=["PUT"])
@login_required
@require_roles("ADMIN")
def update_academic_session(session_id):
    from app.models.academics import AcademicSession, Enrollment, Exam
    from app.models.finance import FeeMaster

    session = AcademicSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Academic session not found"}), 404

    in_use = (
        db.session.query(Enrollment.id).filter_by(session_id=session_id).first()
        or db.session.query(Exam.id).filter_by(session_id=session_id).first()
        or db.session.query(FeeMaster.id).filter_by(session_id=session_id).first()
    )

    if in_use:
        return jsonify({
            "error": "Academic session already in use and cannot be updated"
        }), 409

    data = request.get_json(silent=True) or {}

    if "name" in data:
        session.name = data["name"]
    if "start_date" in data:
        session.start_date = data["start_date"]
    if "end_date" in data:
        session.end_date = data["end_date"]
    if "is_active" in data:
        session.is_active = bool(data["is_active"])

    db.session.commit()
    return jsonify({"message": "Academic session updated"}), 200

@admin_bp.route("/masters/academic-sessions/<int:session_id>", methods=["DELETE"])
@login_required
@require_roles("ADMIN")
def delete_academic_session(session_id):
    from app.models.academics import AcademicSession, Enrollment, Exam
    from app.models.finance import FeeMaster

    session = AcademicSession.query.get(session_id)
    if not session:
        return jsonify({"error": "Academic session not found"}), 404

    in_use = (
        db.session.query(Enrollment.id).filter_by(session_id=session_id).first()
        or db.session.query(Exam.id).filter_by(session_id=session_id).first()
        or db.session.query(FeeMaster.id).filter_by(session_id=session_id).first()
    )

    if in_use:
        return jsonify({
            "error": "Academic session already in use and cannot be deleted"
        }), 409

    db.session.delete(session)
    db.session.commit()
    return jsonify({"message": "Academic session deleted"}), 200



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

@admin_bp.route("/masters/fee-types/<int:fee_type_id>", methods=["GET"])
@login_required
@require_roles("ADMIN")
def get_fee_type(fee_type_id):
    from app.models.finance import FeeType

    fee_type = FeeType.query.get(fee_type_id)
    if not fee_type:
        return jsonify({"error": "Fee type not found"}), 404

    return jsonify({
        "id": fee_type.id,
        "name": fee_type.name,
        "frequency": fee_type.frequency,
    }), 200

@admin_bp.route("/masters/fee-types/<int:fee_type_id>", methods=["PUT"])
@login_required
@require_roles("ADMIN")
def update_fee_type(fee_type_id):
    from app.models.finance import FeeType, FeeMaster

    fee_type = FeeType.query.get(fee_type_id)
    if not fee_type:
        return jsonify({"error": "Fee type not found"}), 404

    if FeeMaster.query.filter_by(fee_type_id=fee_type_id).first():
        return jsonify({
            "error": "Fee type already in use and cannot be updated"
        }), 409

    data = request.get_json(silent=True) or {}

    if "name" in data:
        fee_type.name = data["name"]
    if "frequency" in data:
        fee_type.frequency = data["frequency"]

    db.session.commit()
    return jsonify({"message": "Fee type updated"}), 200


@admin_bp.route("/masters/fee-types/<int:fee_type_id>", methods=["DELETE"])
@login_required
@require_roles("ADMIN")
def delete_fee_type(fee_type_id):
    from app.models.finance import FeeType, FeeMaster

    fee_type = FeeType.query.get(fee_type_id)
    if not fee_type:
        return jsonify({"error": "Fee type not found"}), 404

    if FeeMaster.query.filter_by(fee_type_id=fee_type_id).first():
        return jsonify({
            "error": "Fee type already in use and cannot be deleted"
        }), 409

    db.session.delete(fee_type)
    db.session.commit()
    return jsonify({"message": "Fee type deleted"}), 200



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

@admin_bp.route("/masters/grade-scales/<int:grade_id>", methods=["GET"])
@login_required
@require_roles("ADMIN")
def get_grade_scale(grade_id):
    from app.models.academics import GradeScale

    grade = GradeScale.query.get(grade_id)
    if not grade:
        return jsonify({"error": "Grade scale not found"}), 404

    return jsonify({
        "id": grade.id,
        "grade_name": grade.grade_name,
        "min_percentage": grade.min_percentage,
        "max_percentage": grade.max_percentage,
        "grade_point": grade.grade_point,
    }), 200

@admin_bp.route("/masters/grade-scales/<int:grade_id>", methods=["PUT"])
@login_required
@require_roles("ADMIN")
def update_grade_scale(grade_id):
    from app.models.academics import GradeScale, Marksheet

    grade = GradeScale.query.get(grade_id)
    if not grade:
        return jsonify({"error": "Grade scale not found"}), 404

    if Marksheet.query.filter_by(grade=grade.grade_name).first():
        return jsonify({
            "error": "Grade scale already in use and cannot be updated"
        }), 409

    data = request.get_json(silent=True) or {}

    if "grade_name" in data:
        grade.grade_name = data["grade_name"]
    if "min_percentage" in data:
        grade.min_percentage = data["min_percentage"]
    if "max_percentage" in data:
        grade.max_percentage = data["max_percentage"]
    if "grade_point" in data:
        grade.grade_point = data["grade_point"]

    db.session.commit()
    return jsonify({"message": "Grade scale updated"}), 200

@admin_bp.route("/masters/grade-scales/<int:grade_id>", methods=["DELETE"])
@login_required
@require_roles("ADMIN")
def delete_grade_scale(grade_id):
    from app.models.academics import GradeScale, Marksheet

    grade = GradeScale.query.get(grade_id)
    if not grade:
        return jsonify({"error": "Grade scale not found"}), 404

    if Marksheet.query.filter_by(grade=grade.grade_name).first():
        return jsonify({
            "error": "Grade scale already in use and cannot be deleted"
        }), 409

    db.session.delete(grade)
    db.session.commit()
    return jsonify({"message": "Grade scale deleted"}), 200

