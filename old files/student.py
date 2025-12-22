from app import db
from datetime import datetime
import enum

class Gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class Student(db.Model):
    __tablename__ = 'students'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    admission_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    
    # Academic Info
    grade = db.Column(db.String(20), nullable=False)  # e.g., "Grade 10"
    section = db.Column(db.String(10), nullable=False)  # e.g., "A"
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    guardians = db.relationship('Guardian', backref='student', lazy=True, cascade="all, delete-orphan")
    attendance_records = db.relationship('Attendance', backref='student', lazy=True, cascade="all, delete-orphan")
    results = db.relationship('Result', backref='student', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "admissionId": self.admission_no,
            "name": f"{self.first_name} {self.last_name}",
            "fatherName": self.guardians[0].name if self.guardians else "N/A",
            "grade": self.grade,
            "section": self.section,
            "status": "Active" if self.is_active else "Inactive",
            "dob": self.date_of_birth.isoformat()
        }

class Guardian(db.Model):
    __tablename__ = 'guardians'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50))  # e.g., Father, Mother
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    is_emergency_contact = db.Column(db.Boolean, default=False)

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    exam_date = db.Column(db.Date, nullable=False)

    subject = db.relationship('Subject', backref='results')

    def to_dict(self):
        return {
            "studentId": self.student_id,
            "subject": self.subject.name,
            "marks": self.marks,
            "date": self.exam_date.isoformat()
        }

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # e.g., Present, Absent, Late

    def to_dict(self):
        return {
            "studentId": self.student_id,
            "date": self.date.isoformat(),
            "status": self.status
        }