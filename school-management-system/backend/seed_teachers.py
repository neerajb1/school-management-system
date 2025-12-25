from app import db, create_app
from app.models.users import Staff, Student, Guardian, Role
from app.models.academics import ClassRoom, Enrollment, AcademicSession
from app.models.base import GenderEnum
from datetime import date

app = create_app()

def seed_users():
    with app.app_context():
        session = AcademicSession.query.filter_by(is_current=True).first()
        teacher_role = Role.query.filter_by(name="Teacher").first() or Role(name="Teacher")
        
        # 1. Seed a Sample Teacher
        print("Seeding Staff...")
        head_math = Staff(
            emp_id="TCH-001", 
            first_name="Rajesh", 
            last_name="Kumar",
            email="rajesh.kumar@school.edu",
            role=teacher_role
        )
        db.session.add(head_math)

        # 2. Seed a Sample Student & Guardian
        print("Seeding Student & Enrollment...")
        parent = Guardian(
            father_name="Suresh Sharma",
            parent_email="suresh.sharma@example.com",
            emergency_contact="9876543210"
        )
        db.session.add(parent)
        db.session.flush() # Get parent ID

        # Find Class 10-A (Science Stream)
        class_10a = ClassRoom.query.filter_by(grade="10", section="A").first()

        new_student = Student(
            admission_no="2024-0001",
            first_name="Amit",
            last_name="Sharma",
            dob=date(2009, 8, 14),
            gender=GenderEnum.MALE,
            guardian_id=parent.id
        )
        db.session.add(new_student)
        db.session.flush()

        # 3. Create the Enrollment (Crucial Step)
        enrollment = Enrollment(
            student_id=new_student.id,
            session_id=session.id,
            class_id=class_10a.id,
            roll_no=1,
            status="ACTIVE"
        )
        db.session.add(enrollment)

        db.session.commit()
        print("Phase 2 Success: Staff and Students enrolled!")

if __name__ == "__main__":
    seed_users()