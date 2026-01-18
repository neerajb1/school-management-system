from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
    Text,
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
    GenderEnum,
    TransportMixin,
    MedicalMixin,
)


class Role(BaseModel, TimestampMixin, AuditMixin):
    __tablename__ = "role"

    name = Column(String(50), unique=True, nullable=False)
    # Staff with this role
    staff = relationship(
        "Staff",
        back_populates="role",
        foreign_keys="Staff.role_id"
    )

    users = relationship(
        "UserAccount",
        back_populates="role",
        foreign_keys="UserAccount.role_id"
    )


class Department(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "department"

    name = Column(String(50), unique=True, nullable=False)

    staff = relationship("Staff", back_populates="department")


class Staff(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "staff"

    emp_id = Column(String(30), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    photo_url = Column(String(255))
    joining_date = Column(Date)
    qualification = Column(String(100))

    role_id = Column(BigInteger, ForeignKey("role.id"))
    department_id = Column(BigInteger, ForeignKey("department.id"))

    role = relationship("Role", back_populates="staff")
    department = relationship("Department", back_populates="staff")
    transport = relationship("Transport", back_populates="staff", uselist=False)
    medical = relationship("MedicalRecord", back_populates="staff", uselist=False)
    teacher_assignments = relationship("TeacherAssignment", back_populates="staff")


class Guardian(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "guardian"

    father_name = Column(String(100))
    father_occupation = Column(String(100))
    mother_name = Column(String(100))
    parent_email = Column(String(100))
    emergency_contact = Column(String(20), nullable=False)

    students = relationship("Student", back_populates="guardian")


class Student(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "student"

    admission_no = Column(String(30), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    dob = Column(Date)
    gender = Column(SQLEnum(GenderEnum), nullable=False)
    nationality = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    photo_url = Column(String(255))
    admission_date = Column(Date)

    guardian_id = Column(BigInteger, ForeignKey("guardian.id"))

    guardian = relationship("Guardian", back_populates="students")
    transport = relationship("Transport", back_populates="student", uselist=False)
    medical = relationship("MedicalRecord", back_populates="student", uselist=False)
    enrollments = relationship("Enrollment", back_populates="student")

    def to_dict(self):
        return {
            "id": self.id,
            "admission_no": self.admission_no,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob.isoformat() if self.dob else None,
            "gender": self.gender.value if self.gender else None,
            "nationality": self.nationality,
            "email": self.email,
            "phone": self.phone,
            "photo_url": self.photo_url,
            "admission_date": self.admission_date.isoformat() if self.admission_date else None,
            "guardian_id": self.guardian_id,
        }


class Transport(BaseModel, AuditMixin,TimestampMixin, TransportMixin):
    __tablename__ = "transport_registry"

    student_id = Column(BigInteger, ForeignKey("student.id"), unique=True)
    staff_id = Column(BigInteger, ForeignKey("staff.id"), unique=True)

    student = relationship("Student", back_populates="transport")
    staff = relationship("Staff", back_populates="transport")


class MedicalRecord(BaseModel, AuditMixin,TimestampMixin, MedicalMixin):
    __tablename__ = "medical_registry"

    student_id = Column(BigInteger, ForeignKey("student.id"), unique=True)
    staff_id = Column(BigInteger, ForeignKey("staff.id"), unique=True)

    student = relationship("Student", back_populates="medical")
    staff = relationship("Staff", back_populates="medical")


class School(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "school"

    name = Column(String(100), nullable=False)
    address = Column(Text)
    contact_number = Column(String(20))
    registration_no = Column(String(50))
    logo_url = Column(String(255))


class UserAccount(BaseModel, TimestampMixin, AuditMixin):
    __tablename__ = "user_account"

    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role_id = Column(
        BigInteger,
        ForeignKey("role.id"),
        nullable=False
    )

    user_type = Column(String(20))  # ADMIN / TEACHER / STUDENT / PARENT
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)

    role = relationship(
        "Role",
        back_populates="users",
        foreign_keys=[role_id]
    )



class Announcement(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "announcement"

    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    target_audience = Column(String(20))
    expiry_date = Column(Date)

    session_id = Column(BigInteger, ForeignKey("academic_session.id"))
