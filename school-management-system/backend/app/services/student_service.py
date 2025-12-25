from app.models.users import Student, Guardian
from app.models.academics import Enrollment, Attendance
from app import db
from datetime import datetime

class StudentService:
    @staticmethod
    def register_student(data):
        try:
            # Create the Student object
            new_student = Student(
                admission_no=data['admission_no'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                date_of_birth=datetime.strptime(data['dob'], '%Y-%m-%d'),
                gender=data['gender'].upper(),
                grade=data['grade'],
                section=data['section']
            )
            db.session.add(new_student)
            db.session.flush() # Gets the student ID before committing

            # Create the Guardian object linked to this student
            new_guardian = Guardian(
                student_id=new_student.id,
                name=data['guardian_name'],
                phone=data['guardian_phone'],
                relationship=data.get('relationship', 'Parent')
            )
            db.session.add(new_guardian)
            
            db.session.commit()
            return {"status": "success", "student_id": new_student.id}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}
        
    @staticmethod
    def update_student(student_id, data):
        try:
            student = Student.query.get(student_id)
            if not student:
                return {"status": "error", "message": "Student not found"}

            # Update student fields
            student.first_name = data.get('first_name', student.first_name)
            student.last_name = data.get('last_name', student.last_name)
            student.grade = data.get('grade', student.grade)
            student.section = data.get('section', student.section)
            
            # Update DOB if provided
            if 'dob' in data:
                student.date_of_birth = datetime.strptime(data['dob'], '%Y-%m-%d')

            db.session.commit()
            return {"status": "success", "message": "Student updated"}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}

    @staticmethod
    def delete_student(student_id):
        try:
            student = Student.query.get(student_id)
            if not student:
                return {"status": "error", "message": "Student not found"}
            
            db.session.delete(student)
            db.session.commit()
            return {"status": "success", "message": "Student deleted"}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}

def get_student_by_admission_no(admission_no):
    return Student.query.filter_by(admission_no=admission_no).first()

def create_student(data):
    guardian = Guardian(
        father_name=data.get("father_name"),
        father_occupation=data.get("father_occupation"),
        mother_name=data.get("mother_name"),
        parent_email=data.get("parent_email"),
        emergency_contact=data.get("emergency_contact")
    )
    db.session.add(guardian)
    db.session.flush()  # Flush to get the guardian ID

    student = Student(
        admission_no=data["admission_no"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        dob=data["dob"],
        gender=data["gender"],
        nationality=data["nationality"],
        email=data["email"],
        phone=data["phone"],
        photo_url=data.get("photo_url"),
        admission_date=data["admission_date"],
        guardian_id=guardian.id
    )
    db.session.add(student)
    db.session.commit()
    return student

def get_student_enrollments(student_id):
    return Enrollment.query.filter_by(student_id=student_id).all()

def get_student_attendance(student_id):
    return Attendance.query.join(Enrollment).filter(Enrollment.student_id == student_id).all()