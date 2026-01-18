# backend/models/refresh_token.py

from datetime import datetime
from app.extensions import db

class RefreshToken(db.Model):
    __tablename__ = "refresh_token"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    jti = db.Column(db.String(255), nullable=False, unique=True, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_revoked = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    created_by_id = db.Column(db.Integer, nullable=True)
    updated_by_id = db.Column(db.Integer, nullable=True)
