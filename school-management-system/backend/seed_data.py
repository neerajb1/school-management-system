from app import db, create_app
from app.models.users import Role, Department, Staff, Student, Guardian
from app.models.academics import AcademicSession, ClassRoom, Enrollment
from app.models.base import GenderEnum
from datetime import date

app = create_app()

def seed_production_data():
    with app.app_context():
        # 1. FETCH INFRASTRUCTURE
        current_session = AcademicSession.query.filter_by(is_current=True).first()
        
        # 2. ROBUST ROLE SEEDING (Get or Create)
        print("Checking Roles...")
        admin_role = Role.query.filter_by(name="Administrator").first()
        if not admin_role:
            admin_role = Role(name="Administrator")
            db.session.add(admin_role)

        teacher_role = Role.query.filter_by(name="Teacher").first()
        if not teacher_role:
            teacher_role = Role(name="Teacher")
            db.session.add(teacher_role)

        # 3. ROBUST DEPARTMENT SEEDING
        science_dept = Department.query.filter_by(name="Science").first()
        if not science_dept:
            science_dept = Department(name="Science")
            db.session.add(science_dept)
        
        # Flush here to ensure we have IDs for the next steps
        db.session.flush()

        # 4. SEED STAFF (Use unique emp_id to avoid same error here)
        print("Seeding Staff...")
        if not Staff.query.filter_by(emp_id="TCH2024001").first():
            teacher = Staff(
                emp_id="TCH2024001",
                first_name="Arjun",
                last_name="Mehta",
                email="arjun.mehta@school.in",
                role_id=teacher_role.id,
                department_id=science_dept.id
            )
            db.session.add(teacher)

        # 5. SEED GUARDIAN & STUDENT
        print("Seeding Students...")
        # Check if student already exists
        if not Student.query.filter_by(admission_no="ADM2024001").first():
            parent = Guardian(
                father_name="Vikram Sharma",
                mother_name="Priya Sharma",
                parent_email="sharma.family@example.com",
                emergency_contact="9876543210"
            )
            db.session.add(parent)
            db.session.flush()

            class_10a = ClassRoom.query.filter_by(grade="10", section="A").first()

            student = Student(
                admission_no="ADM2024001",
                first_name="Rohan",
                last_name="Sharma",
                dob=date(2009, 5, 20),
                gender=GenderEnum.MALE,
                guardian_id=parent.id
            )
            db.session.add(student)
            db.session.flush()

            # 6. ENROLLMENT
            enrollment = Enrollment(
                student_id=student.id,
                session_id=current_session.id,
                class_id=class_10a.id,
                roll_no=1,
                status="ACTIVE"
            )
            db.session.add(enrollment)

        db.session.commit()
        print("Success: Phase 2 data synced without duplicates!")

if __name__ == "__main__":
    seed_production_data()