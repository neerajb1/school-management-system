from app.models.base import db, BaseModel, TimestampMixin, AttendanceStatusEnum, AttendanceTypeEnum

class AcademicSession(BaseModel, TimestampMixin):
    __tablename__ = "academic_session"
    year_label = db.Column(db.String(20), unique=True, nullable=False)
    is_current = db.Column(db.Boolean, default=False)

    enrollments = db.relationship("Enrollment", back_populates="session")
    exams = db.relationship("Exam", back_populates="session")
    teacher_assignments = db.relationship("TeacherAssignment", back_populates="session")
    fee_masters = db.relationship("FeeMaster", back_populates="session")

class Subject(BaseModel, TimestampMixin):
    __tablename__ = "subject"
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)

    marksheets = db.relationship("Marksheet", back_populates="subject")
    teacher_assignments = db.relationship("TeacherAssignment", back_populates="subject")

class ClassRoom(BaseModel, TimestampMixin):
    __tablename__ = "class"
    grade = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(5), nullable=False)
    stream = db.Column(db.String(20), default="General")

    enrollments = db.relationship("Enrollment", back_populates="class_room")
    teacher_assignments = db.relationship("TeacherAssignment", back_populates="class_room")

class Enrollment(BaseModel, TimestampMixin):
    __tablename__ = "enrollment"
    student_id = db.Column(db.BigInteger, db.ForeignKey("student.id"), nullable=False)
    session_id = db.Column(db.BigInteger, db.ForeignKey("academic_session.id"), nullable=False)
    class_id = db.Column(db.BigInteger, db.ForeignKey("class.id"), nullable=False)
    roll_no = db.Column(db.Integer)
    status = db.Column(db.String(20))

    # Define the relationship with the Student model
    student = db.relationship("Student", back_populates="enrollments")  # Ensure this relationship exists

    session = db.relationship("AcademicSession", back_populates="enrollments")
    class_room = db.relationship("ClassRoom", back_populates="enrollments")
    attendance_records = db.relationship("Attendance", back_populates="enrollment")
    marksheets = db.relationship("Marksheet", back_populates="enrollment")
    ledgers = db.relationship("StudentLedger", back_populates="enrollment")

class Attendance(BaseModel, TimestampMixin):
    __tablename__ = "attendance"
    enrollment_id = db.Column(db.BigInteger, db.ForeignKey("enrollment.id"), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(AttendanceStatusEnum), nullable=False)
    attendance_type = db.Column(db.Enum(AttendanceTypeEnum))
    attendance_remarks = db.Column(db.Text)

    enrollment = db.relationship("Enrollment", back_populates="attendance_records")

class Exam(BaseModel, TimestampMixin):
    __tablename__ = "exam"
    session_id = db.Column(db.BigInteger, db.ForeignKey("academic_session.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    term = db.Column(db.String(20))
    exam_type = db.Column(db.String(20))
    description = db.Column(db.Text)
    #start_date = db.Column(db.Date, nullable=False)  # Added start_date column
    #end_date = db.Column(db.Date, nullable=False)    # Added end_date column

    session = db.relationship("AcademicSession", back_populates="exams")
    marksheets = db.relationship("Marksheet", back_populates="exam")

class Marksheet(BaseModel, TimestampMixin):
    __tablename__ = "marksheet"
    enrollment_id = db.Column(db.BigInteger, db.ForeignKey("enrollment.id"), nullable=False)
    subject_id = db.Column(db.BigInteger, db.ForeignKey("subject.id"), nullable=False)
    exam_id = db.Column(db.BigInteger, db.ForeignKey("exam.id"), nullable=False)
    marks_obtained = db.Column(db.Numeric(5, 2))
    total_marks = db.Column(db.Numeric(5, 2))
    is_locked = db.Column(db.Boolean, default=False)

    enrollment = db.relationship("Enrollment", back_populates="marksheets")
    subject = db.relationship("Subject", back_populates="marksheets")
    exam = db.relationship("Exam", back_populates="marksheets")

class TeacherAssignment(BaseModel, TimestampMixin):
    __tablename__ = "teacher_assignment"
    staff_id = db.Column(db.BigInteger, db.ForeignKey("staff.id"), nullable=False)
    class_id = db.Column(db.BigInteger, db.ForeignKey("class.id"), nullable=False)
    subject_id = db.Column(db.BigInteger, db.ForeignKey("subject.id"), nullable=False)
    session_id = db.Column(db.BigInteger, db.ForeignKey("academic_session.id"), nullable=False)

    staff = db.relationship("Staff", back_populates="teacher_assignments")
    subject = db.relationship("Subject", back_populates="teacher_assignments")
    session = db.relationship("AcademicSession", back_populates="teacher_assignments")
    class_room = db.relationship("ClassRoom", back_populates="teacher_assignments")
