from app.extensions import db
from app.models.academics import Subject


def create_subject_service(admin_user_id: int, data: dict) -> Subject:
    name = data.get("name")
    code = data.get("code")

    if not name:
        raise ValueError("name is required")

    if not code:
        raise ValueError("code is required")

    existing = (
        db.session.query(Subject)
        .filter(Subject.code == code)
        .first()
    )
    if existing:
        raise ValueError("Subject code already exists")

    subject = Subject(
        name=name.strip(),
        code=code.strip().upper(),
        created_by_id=admin_user_id,
        updated_by_id=admin_user_id,
    )

    db.session.add(subject)
    return subject
