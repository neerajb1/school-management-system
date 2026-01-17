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

class DiscountOffer(BaseModel, TimestampMixin):
    """
    Stores various offers: 'SIBLING', 'SCHOLARSHIP', 'STAFF_CHILD', or 'EARLY_BIRD'.
    """
    __tablename__ = "discount_offer"
    name = db.Column(db.String(50), nullable=False) # e.g., "Sibling Discount"
    code = db.Column(db.String(20), unique=True)
    discount_percent = db.Column(db.Numeric(5, 2), default=0.00)
    flat_discount = db.Column(db.Numeric(10, 2), default=0.00)
    is_active = db.Column(db.Boolean, default=True)


class StudentLedger(BaseModel, TimestampMixin):
    __tablename__ = "student_ledger"
    enrollment_id = db.Column(db.BigInteger, db.ForeignKey("enrollment.id"), nullable=False)
    fee_master_id = db.Column(db.BigInteger, db.ForeignKey("fee_master.id"), nullable=False)
    offer_id = db.Column(db.BigInteger, db.ForeignKey("discount_offer.id"), nullable=True)
    total_base_amount = db.Column(db.Numeric(10, 2), nullable=False)
    discount_amount = db.Column(db.Numeric(10, 2))
    final_payable_amount = db.Column(db.Numeric(10, 2), nullable=False) # After discount
    # Status: 'PENDING', 'PARTIAL', 'PAID', 'OVERDUE'
    status = db.Column(db.String(20), default="PENDING")

    enrollment = db.relationship("Enrollment", back_populates="ledgers")
    fee_master = db.relationship("FeeMaster", back_populates="ledgers")
    installments = db.relationship("FeeInstallment", back_populates="ledger", cascade="all, delete-orphan")

class FeeInstallment(BaseModel, TimestampMixin):
    __tablename__ = "fee_installment"

    id = db.Column(db.String, primary_key=True)

    fee_master_id = db.Column(
        db.ForeignKey("fee_master.id"),
        nullable=False,
        index=True
    )

    student_id = db.Column(
        db.ForeignKey("student.id"),
        nullable=False,
        index=True
    )

    due_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    status = db.Column(
        db.Enum("DUE", "PAID", "OVERDUE", name="fee_status_enum"),
        nullable=False,
        default="DUE"
    )

    student = db.relationship("Student", backref="fee_installments")
    fee_master = db.relationship("FeeMaster", backref="installments")

    
class Transaction(BaseModel, TimestampMixin):
    __tablename__ = "transaction"
    # Now link transaction directly to an installment
    installment_id = db.Column(db.BigInteger, db.ForeignKey("fee_installment.id"), nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum(PaymentMethodEnum), nullable=False)
    transaction_ref = db.Column(db.String(100)) # UPI ID, Bank Ref No, or Receipt No
    
    installment = db.relationship("FeeInstallment", back_populates="transactions")


