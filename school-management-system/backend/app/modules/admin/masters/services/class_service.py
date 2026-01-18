from app.extensions import db
from sqlalchemy import text
from app.models.academics import ClassRoom

def create_class_service(*, admin_user_id: int, data: dict):
    name = data.get("name")
    section = data.get("section")

    if not name:
        raise ValueError("name is required")

    exists = (
        db.session.query(ClassRoom)
        .filter_by(name=name, section=section)
        .first()
    )
    if exists:
        raise ValueError("Class already exists")

    cls = ClassRoom(
        name=name,
        section=section,
        created_by_id=admin_user_id,
    )

    db.session.add(cls)
    return cls
