from app.models.base import db, BaseModel, TimestampMixin, FeeFrequencyEnum, PaymentMethodEnum

class FeeType(BaseModel, TimestampMixin):
    __tablename__ = "fee_type"
    name = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.Enum(FeeFrequencyEnum), nullable=False)
    fee_masters = db.relationship("FeeMaster", back_populates="fee_type")

class FeeMaster(BaseModel, TimestampMixin):
    __tablename__ = "fee_master"
    fee_type_id = db.Column(db.BigInteger, db.ForeignKey("fee_type.id"), nullable=False)
    class_id = db.Column(db.BigInteger, db.ForeignKey("class.id"), nullable=False)
    session_id = db.Column(db.BigInteger, db.ForeignKey("academic_session.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    fee_type = db.relationship("FeeType", back_populates="fee_masters")
    session = db.relationship("AcademicSession", back_populates="fee_masters")
    ledgers = db.relationship("StudentLedger", back_populates="fee_master")

class StudentLedger(BaseModel, TimestampMixin):
    __tablename__ = "student_ledger"
    enrollment_id = db.Column(db.BigInteger, db.ForeignKey("enrollment.id"), nullable=False)
    fee_master_id = db.Column(db.BigInteger, db.ForeignKey("fee_master.id"), nullable=False)
    discount_amount = db.Column(db.Numeric(10, 2))
    final_amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20))

    enrollment = db.relationship("Enrollment", back_populates="ledgers")
    fee_master = db.relationship("FeeMaster", back_populates="ledgers")

    # Define the reverse relationship to Transaction
    transactions = db.relationship("Transaction", back_populates="ledger")  # Added relationship

class Transaction(BaseModel, TimestampMixin):
    __tablename__ = "transaction"
    ledger_id = db.Column(db.BigInteger, db.ForeignKey("student_ledger.id"), nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum(PaymentMethodEnum), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)

    ledger = db.relationship("StudentLedger", back_populates="transactions")
