import json
from app import db
from app.models.users import Student, Guardian, Staff
from app.models.academics import Subject, Enrollment, Attendance, TeacherAssignment, AcademicSession
from app.models.finance import FeeType, FeeMaster, StudentLedger, Transaction

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def migrate_subjects():
    subjects = load_json('public/api/config.json')["subjects"]
    for subject_name in subjects:
        subject = Subject(name=subject_name)
        db.session.add(subject)
    db.session.commit()

def migrate_results():
    results = load_json('public/api/results.json')
    for result in results:
        student = Student.query.filter_by(admission_no=result["studentId"]).first()
        subject = Subject.query.filter_by(name=result["subject"]).first()
        if student and subject:
            db.session.add(Marksheet(
                enrollment_id=result["enrollmentId"],
                subject_id=subject.id,
                marks_obtained=result["marks"],
                total_marks=result["totalMarks"]
            ))
    db.session.commit()

def migrate_attendance():
    attendance_records = load_json('public/api/attendance.json')
    for record in attendance_records:
        for student_record in record["records"]:
            enrollment = Enrollment.query.filter_by(id=student_record["enrollmentId"]).first()
            if enrollment:
                db.session.add(Attendance(
                    enrollment_id=enrollment.id,
                    attendance_date=record["date"],
                    status=student_record["status"],
                    attendance_type=student_record.get("type", "FULL_DAY")
                ))
    db.session.commit()

def migrate_teacher_assignments(data):
    for record in data:
        session = AcademicSession.query.filter_by(year_label=record["session"]).first()
        if not session:
            print(f"Skipping record: AcademicSession '{record['session']}' not found.")
            continue

        class_room = ClassRoom.query.filter_by(grade=record["grade"], section=record["section"]).first()
        if not class_room:
            print(f"Skipping record: Class '{record['grade']} {record['section']}' not found.")
            continue

        subject = Subject.query.filter_by(name=record["subject"]).first()
        if not subject:
            print(f"Skipping record: Subject '{record['subject']}' not found.")
            continue

        staff = Staff.query.filter_by(emp_id=record["teacher_emp_id"]).first()
        if not staff:
            print(f"Skipping record: Staff with emp_id '{record['teacher_emp_id']}' not found.")
            continue

        teacher_assignment = TeacherAssignment(
            staff_id=staff.id,
            class_id=class_room.id,
            subject_id=subject.id,
            session_id=session.id
        )
        db.session.add(teacher_assignment)

    db.session.commit()
    print("Teacher assignments migrated successfully.")
