from app.models.base import db, BaseModel, TimestampMixin, GenderEnum, TransportMixin, MedicalMixin

class Role(BaseModel, TimestampMixin):
    __tablename__ = "role"
    name = db.Column(db.String(50), unique=True, nullable=False)

    staff = db.relationship("Staff", back_populates="role")

class Department(BaseModel, TimestampMixin):
    __tablename__ = "department"
    name = db.Column(db.String(50), unique=True, nullable=False)

    staff = db.relationship("Staff", back_populates="department")

class Staff(BaseModel, TimestampMixin):
    __tablename__ = "staff"
    emp_id = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    photo_url = db.Column(db.String(255))

    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"))
    department_id = db.Column(db.BigInteger, db.ForeignKey("department.id"))

    role = db.relationship("Role", back_populates="staff")
    department = db.relationship("Department", back_populates="staff")
    transport = db.relationship("Transport", back_populates="staff", uselist=False)
    medical = db.relationship("MedicalRecord", back_populates="staff", uselist=False)
    teacher_assignments = db.relationship("TeacherAssignment", back_populates="staff")

class Guardian(BaseModel, TimestampMixin):
    """Handles Parent/Guardian info for one or more siblings"""
    __tablename__ = "guardian"
    father_name = db.Column(db.String(100))
    father_occupation = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    parent_email = db.Column(db.String(100))
    emergency_contact = db.Column(db.String(20), nullable=False)
    
    # Relationship: One guardian can have multiple students (siblings)
    students = db.relationship("Student", back_populates="guardian")

class Student(BaseModel, TimestampMixin):
    __tablename__ = "student"
    admission_no = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum(GenderEnum), nullable=False)
    nationality = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    photo_url = db.Column(db.String(255))
    admission_date = db.Column(db.Date)

    # Foreign Keys to specialized tables
    guardian_id = db.Column(db.BigInteger, db.ForeignKey("guardian.id"))

    # Relationships
    guardian = db.relationship("Guardian", back_populates="students")
    transport = db.relationship("Transport", back_populates="student", uselist=False)
    medical = db.relationship("MedicalRecord", back_populates="student", uselist=False)
    enrollments = db.relationship("Enrollment", back_populates="student")

    def to_dict(self):
        """Convert the Student object to a dictionary."""
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

class Transport(BaseModel, TimestampMixin, TransportMixin):
    __tablename__ = "transport_registry"
    student_id = db.Column(db.BigInteger, db.ForeignKey("student.id"), nullable=True, unique=True)
    staff_id = db.Column(db.BigInteger, db.ForeignKey("staff.id"), nullable=True, unique=True)

    student = db.relationship("Student", back_populates="transport")
    staff = db.relationship("Staff", back_populates="transport")

class MedicalRecord(BaseModel, TimestampMixin, MedicalMixin):
    __tablename__ = "medical_registry"
    student_id = db.Column(db.BigInteger, db.ForeignKey("student.id"), nullable=True, unique=True)
    staff_id = db.Column(db.BigInteger, db.ForeignKey("staff.id"), nullable=True, unique=True)

    student = db.relationship("Student", back_populates="medical")
    staff = db.relationship("Staff", back_populates="medical")
