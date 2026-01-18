# app/core/crud_base.py

from typing import Any, Dict, List, Optional, Type
from app.extensions import db


class CRUDBase:
    """
    Reusable CRUD base for SQLAlchemy models.

    - Uses explicit db.session queries
    - No Flask request/response
    - No permissions
    """

    def __init__(self, model: Type[Any]):
        if model is None:
            raise ValueError("CRUDBase requires a model")
        self.model = model

    # ----------------------------
    # Read
    # ----------------------------
    def get_by_id(self, obj_id: int):
        return (
            db.session.query(self.model)
            .filter(self.model.id == obj_id)
            .first()
        )

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        query = db.session.query(self.model)

        if filters:
            query = query.filter_by(**filters)

        return query.offset(offset).limit(limit).all()

    # ----------------------------
    # Create
    # ----------------------------
    def create(self, data: Dict[str, Any]):
        obj = self.model(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    # ----------------------------
    # Update
    # ----------------------------
    def update(self, obj: Any, data: Dict[str, Any]):
        for key, value in data.items():
            setattr(obj, key, value)

        db.session.commit()
        return obj

    # ----------------------------
    # Delete
    # ----------------------------
    def delete(self, obj: Any):
        db.session.delete(obj)
        db.session.commit()
