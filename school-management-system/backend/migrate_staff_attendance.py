import json
import os
from datetime import datetime
from app import db
from app.models.users import Staff, Role, Department, Student
from app.models.academics import Enrollment, Attendance, AcademicSession
from app.models.base import AttendanceStatusEnum, AttendanceTypeEnum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the base directory for JSON files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def migrate_staff():
    logging.info("Starting Staff Migration...")
    teachers_file = os.path.join(BASE_DIR, 'public', 'api', 'teachers.json')  # Updated path
    with open(teachers_file, 'r') as f:
        teachers_data = json.load(f)

    # Cache departments and roles to avoid redundant queries
    department_cache = {dept.name: dept for dept in Department.query.all()}
    role_cache = {role.name: role for role in Role.query.all()}

    for data in teachers_data:
        # 1. Get or Create Department
        dept_name = data.get('department', 'General')
        if dept_name not in department_cache:
            dept = Department(name=dept_name)
            db.session.add(dept)
            db.session.flush()  # Persist the department to get its ID
            department_cache[dept_name] = dept
        else:
            dept = department_cache[dept_name]

        # 2. Get or Create Role
        role_name = 'Teacher'
        if role_name not in role_cache:
            role = Role(name=role_name)
            db.session.add(role)
            db.session.flush()  # Persist the role to get its ID
            role_cache[role_name] = role
        else:
            role = role_cache[role_name]

        # 3. Create Staff Member
        names = data['full_name'].split(' ', 1)
        staff = Staff(
            emp_id=data['employee_id'],
            first_name=names[0],
            last_name=names[1] if len(names) > 1 else "",
            email=data['email'],
            phone=data.get('phone'),
            department_id=dept.id,
            role_id=role.id
        )
        db.session.add(staff)
    
    db.session.commit()
    logging.info("Staff Migration Successful!")

def migrate_attendance():
    logging.info("Starting Attendance Migration...")
    attendance_file = os.path.join(BASE_DIR, 'public', 'api', 'attendance.json')  # Updated path
    with open(attendance_file, 'r') as f:
        attendance_data = json.load(f)

    # Cache academic sessions to avoid redundant queries
    session_cache = {session.id: session for session in AcademicSession.query.all()}

    for record in attendance_data:
        # 1. Find the Student by Admission ID
        student = Student.query.filter_by(admission_no=record['admissionId']).first()
        if not student:
            logging.warning(f"Skipping: Student {record['admissionId']} not found.")
            continue

        # 2. Find their Current Enrollment
        enrollment = Enrollment.query.filter_by(student_id=student.id).first()
        if not enrollment:
            logging.warning(f"Skipping: No active enrollment for {student.first_name}")
            continue

        # 3. Map JSON status to our Enum
        status_map = {
            "Present": AttendanceStatusEnum.PRESENT,
            "Absent": AttendanceStatusEnum.ABSENT,
            "Late": AttendanceStatusEnum.LATE,
            "Leave": AttendanceStatusEnum.LEAVE
        }
        attendance_status = status_map.get(record['status'], AttendanceStatusEnum.PRESENT)

        # 4. Parse the attendance date
        try:
            attendance_date = datetime.strptime(record['date'], '%Y-%m-%d').date()
        except ValueError:
            logging.error(f"Invalid date format for record: {record}")
            continue

        # 5. Create Attendance Record
        attendance = Attendance(
            enrollment_id=enrollment.id,
            attendance_date=attendance_date,
            status=attendance_status,
            attendance_remarks=record.get('remarks')
        )
        db.session.add(attendance)

    db.session.commit()
    logging.info("Attendance Migration Successful!")

if __name__ == "__main__":
    # Note: migrate_students() should be run BEFORE this
    migrate_staff()
    migrate_attendance()