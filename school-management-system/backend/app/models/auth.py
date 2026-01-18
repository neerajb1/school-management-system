from sqlalchemy import Column, String
from app.extensions import db
from app.models.base import BaseModel, TimestampMixin


class RevokedToken(BaseModel, TimestampMixin):
    __tablename__ = "revoked_token"

    jti = Column(String(36), unique=True, nullable=False)
    reason = Column(String(100), nullable=True)
