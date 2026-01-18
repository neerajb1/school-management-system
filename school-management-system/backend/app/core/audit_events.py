from sqlalchemy import event
from sqlalchemy.orm import Mapper
from app.extensions import db
from app.core.audit_context import get_current_user_id

def register_audit_events():
    for mapper in db.Model.registry.mappers:
        cls = mapper.class_

        if hasattr(cls, "created_by_id"):
            event.listen(cls, "before_insert", _before_insert)
        if hasattr(cls, "updated_by_id"):
            event.listen(cls, "before_update", _before_update)

def _before_insert(mapper, connection, target):
    user_id = get_current_user_id()
    if user_id:
        if hasattr(target, "created_by_id") and not target.created_by_id:
            target.created_by_id = user_id
        if hasattr(target, "updated_by_id"):
            target.updated_by_id = user_id

def _before_update(mapper, connection, target):
    user_id = get_current_user_id()
    if user_id and hasattr(target, "updated_by_id"):
        target.updated_by_id = user_id
