from app.extensions import db
from app.models.academics import GradeScale


def create_grade_scale_service(admin_user_id: int, data: dict) -> GradeScale:
    grade_name = data.get("grade_name")
    min_percentage = data.get("min_percentage")
    max_percentage = data.get("max_percentage")

    if not grade_name:
        raise ValueError("grade_name is required")

    if min_percentage is None or max_percentage is None:
        raise ValueError("min_percentage and max_percentage are required")

    if min_percentage > max_percentage:
        raise ValueError("min_percentage cannot be greater than max_percentage")

    grade = GradeScale(
        grade_name=grade_name.strip(),
        min_percentage=min_percentage,
        max_percentage=max_percentage,
        remarks=data.get("remarks"),
        created_by_id=admin_user_id,
        updated_by_id=admin_user_id,
    )

    db.session.add(grade)
    return grade
