from sqlalchemy import (
    Column,
    String,
    Date,
    Numeric,
    Boolean,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, AuditMixin, TimestampMixin


class AcademicSession(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "academic_session"

    name = Column(String(50), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)

    enrollments = relationship("Enrollment", back_populates="session")
    exams = relationship("Exam", back_populates="session")
    teacher_assignments = relationship("TeacherAssignment", back_populates="session")
    fee_masters = relationship("FeeMaster", back_populates="session")


class Subject(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "subject"

    name = Column(String(50), nullable=False)
    code = Column(String(20), unique=True, nullable=False)

    marksheets = relationship("Marksheet", back_populates="subject")
    teacher_assignments = relationship("TeacherAssignment", back_populates="subject")


class ClassRoom(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "class_room"

    name = Column(String(50), nullable=False)
    section = Column(String(10))

    enrollments = relationship("Enrollment", back_populates="class_room")
    teacher_assignments = relationship("TeacherAssignment", back_populates="class_room")
    fee_masters = relationship("FeeMaster", back_populates="class_room")


class Enrollment(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "enrollment"

    student_id = Column(BigInteger, ForeignKey("student.id"), nullable=False)
    class_id = Column(BigInteger, ForeignKey("class_room.id"), nullable=False)
    session_id = Column(BigInteger, ForeignKey("academic_session.id"), nullable=False)
    roll_no = Column(String(20))

    student = relationship("Student", back_populates="enrollments")
    class_room = relationship("ClassRoom", back_populates="enrollments")
    session = relationship("AcademicSession", back_populates="enrollments")
    attendance_records = relationship("Attendance", back_populates="enrollment")
    marksheets = relationship("Marksheet", back_populates="enrollment")
    ledgers = relationship("StudentLedger", back_populates="enrollment")


class Attendance(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "attendance"

    enrollment_id = Column(BigInteger, ForeignKey("enrollment.id"), nullable=False)
    date = Column(Date, nullable=False)
    is_present = Column(Boolean, default=True)

    enrollment = relationship("Enrollment", back_populates="attendance_records")


class Exam(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "exam"

    name = Column(String(50), nullable=False)
    session_id = Column(BigInteger, ForeignKey("academic_session.id"), nullable=False)

    session = relationship("AcademicSession", back_populates="exams")
    marksheets = relationship("Marksheet", back_populates="exam")


class Marksheet(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "marksheet"

    enrollment_id = Column(BigInteger, ForeignKey("enrollment.id"), nullable=False)
    subject_id = Column(BigInteger, ForeignKey("subject.id"), nullable=False)
    exam_id = Column(BigInteger, ForeignKey("exam.id"), nullable=False)

    marks_obtained = Column(Numeric(5, 2))
    max_marks = Column(Numeric(5, 2))
    grade = Column(String(10))

    enrollment = relationship("Enrollment", back_populates="marksheets")
    subject = relationship("Subject", back_populates="marksheets")
    exam = relationship("Exam", back_populates="marksheets")


class TeacherAssignment(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "teacher_assignment"

    staff_id = Column(BigInteger, ForeignKey("staff.id"), nullable=False)
    subject_id = Column(BigInteger, ForeignKey("subject.id"), nullable=False)
    class_id = Column(BigInteger, ForeignKey("class_room.id"), nullable=False)
    session_id = Column(BigInteger, ForeignKey("academic_session.id"), nullable=False)

    staff = relationship("Staff", back_populates="teacher_assignments")
    subject = relationship("Subject", back_populates="teacher_assignments")
    class_room = relationship("ClassRoom", back_populates="teacher_assignments")
    session = relationship("AcademicSession", back_populates="teacher_assignments")


class GradeScale(BaseModel, AuditMixin,TimestampMixin):
    __tablename__ = "grade_scale"

    grade_name = Column(String(10), nullable=False)
    min_percentage = Column(Numeric(5, 2), nullable=False)
    max_percentage = Column(Numeric(5, 2), nullable=False)
    grade_point = Column(Numeric(3, 1))
    remarks = Column(String(100))
