from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    BigInteger,
    DateTime,
    String,
    Text,
    Enum as SQLEnum,
)
from sqlalchemy.orm import DeclarativeBase


# =======================
# BASE
# =======================

class Base(DeclarativeBase):
    pass


# =======================
# ENUMS (ALL OF THEM)
# =======================

class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class TransportTypeEnum(Enum):
    BUS = "bus"
    VAN = "van"
    WALKING = "walking"


class BloodGroupEnum(Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    O_POS = "O+"
    O_NEG = "O-"
    AB_POS = "AB+"
    AB_NEG = "AB-"


class FeeFrequencyEnum(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class PaymentMethodEnum(Enum):
    CASH = "cash"
    CARD = "card"
    UPI = "upi"
    BANK_TRANSFER = "bank_transfer"


# =======================
# MIXINS
# =======================

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

class AuditMixin:
    created_by_id = Column(
        BigInteger,
        ForeignKey("user_account.id"),
        nullable=True
    )
    updated_by_id = Column(
        BigInteger,
        ForeignKey("user_account.id"),
        nullable=True
    )


class TransportMixin:
    transport_type = Column(SQLEnum(TransportTypeEnum), nullable=True)
    transport_route = Column(String(100), nullable=True)


class MedicalMixin:
    blood_group = Column(SQLEnum(BloodGroupEnum), nullable=True)
    medical_notes = Column(Text, nullable=True)


# =======================
# BASE MODEL
# =======================

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
