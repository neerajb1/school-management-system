from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
    Numeric,
    Boolean,
    BigInteger,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship

from app.models.base import (
    BaseModel,
    AuditMixin,
    TimestampMixin,
    FeeFrequencyEnum,
    PaymentMethodEnum,
)


class FeeType(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "fee_type"

    name = Column(String(50), nullable=False)
    frequency = Column(SQLEnum(FeeFrequencyEnum), nullable=False)

    fee_masters = relationship("FeeMaster", back_populates="fee_type")


class FeeMaster(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "fee_master"

    class_id = Column(BigInteger, ForeignKey("class_room.id"), nullable=False)
    session_id = Column(BigInteger, ForeignKey("academic_session.id"), nullable=False)
    fee_type_id = Column(BigInteger, ForeignKey("fee_type.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(Date)

    fee_type = relationship("FeeType", back_populates="fee_masters")
    session = relationship("AcademicSession", back_populates="fee_masters")
    class_room = relationship("ClassRoom", back_populates="fee_masters")

class DiscountOffer(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "discount_offer"

    name = Column(String(100), nullable=False)
    discount_percentage = Column(Numeric(5, 2))
    discount_amount = Column(Numeric(10, 2))
    valid_from = Column(Date)
    valid_to = Column(Date)
    is_active = Column(Boolean, default=True)

    ledgers = relationship("StudentLedger", back_populates="discount_offer")


class StudentLedger(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "student_ledger"

    enrollment_id = Column(BigInteger, ForeignKey("enrollment.id"), nullable=False)
    fee_master_id = Column(BigInteger, ForeignKey("fee_master.id"), nullable=False)
    discount_offer_id = Column(BigInteger, ForeignKey("discount_offer.id"))

    original_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2))
    final_amount = Column(Numeric(10, 2), nullable=False)
    is_paid = Column(Boolean, default=False)

    enrollment = relationship("Enrollment", back_populates="ledgers")
    fee_master = relationship("FeeMaster")
    discount_offer = relationship("DiscountOffer", back_populates="ledgers")
    installments = relationship("FeeInstallment", back_populates="ledger")


class FeeInstallment(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "fee_installment"

    ledger_id = Column(BigInteger, ForeignKey("student_ledger.id"), nullable=False)
    installment_no = Column(BigInteger, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(Date)
    is_paid = Column(Boolean, default=False)

    ledger = relationship("StudentLedger", back_populates="installments")
    transactions = relationship("Transaction", back_populates="installment")


class Transaction(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "transaction"

    installment_id = Column(BigInteger, ForeignKey("fee_installment.id"), nullable=False)
    payment_date = Column(DateTime)
    amount_paid = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(SQLEnum(PaymentMethodEnum), nullable=False)
    reference_no = Column(String(100))

    installment = relationship("FeeInstallment", back_populates="transactions")
