from app.extensions import db
from app.models.academics import AcademicSession


def create_academic_session_service(admin_user_id: int, data: dict) -> AcademicSession:
    name = data.get("name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not name:
        raise ValueError("name is required")

    session = AcademicSession(
        name=name.strip(),
        start_date=start_date,
        end_date=end_date,
        is_active=False,
        created_by_id=admin_user_id,
        updated_by_id=admin_user_id,
    )

    db.session.add(session)
    return session
