from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

# Enums
class GenderEnum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class AttendanceStatusEnum(enum.Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"

class AttendanceTypeEnum(enum.Enum):
    FULL_DAY = "FULL_DAY"
    HALF_DAY = "HALF_DAY"
    LATE = "LATE"
    LEAVE = "LEAVE"

class FeeFrequencyEnum(enum.Enum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"
    ONETIME = "ONETIME"

class PaymentMethodEnum(enum.Enum):
    CASH = "CASH"
    CARD = "CARD"
    UPI = "UPI"
    BANK_TRANSFER = "BANK_TRANSFER"

# Base Mixins
class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.BigInteger)
    modified_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    modified_by = db.Column(db.BigInteger)
    is_deleted = db.Column(db.Boolean, default=False)

class TransportMixin:
    transport_type = db.Column(db.String(50)) # School Bus, Private, Walk
    bus_route = db.Column(db.String(50))
    pickup_point = db.Column(db.String(100))

class MedicalMixin:
    blood_group = db.Column(db.String(5))
    medical_conditions = db.Column(db.Text)
    allergies = db.Column(db.Text)

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
