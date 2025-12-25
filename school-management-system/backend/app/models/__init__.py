# File: /school-management-system/backend/app/models/__init__.py
from app.models.base import db
from app.models.users import Role, Department, Staff, Student
from app.models.academics import (
    AcademicSession,
    Subject,
    ClassRoom,
    Enrollment,
    Attendance,
    Exam,
    Marksheet,
    TeacherAssignment,
)
from app.models.finance import FeeType, FeeMaster, StudentLedger, Transaction