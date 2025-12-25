import random
from datetime import date
from faker import Faker
from app import db, create_app
from app.models.users import Student, Guardian
from app.models.academics import ClassRoom, Enrollment, AcademicSession
from app.models.base import GenderEnum

app = create_app()
fake = Faker('en_IN')

def bulk_seed_students(students_per_class=10):
    with app.app_context():
        print(f"Updating bulk seed with nationality and admission dates...")
        
        session = AcademicSession.query.filter_by(is_current=True).first()
        all_classes = ClassRoom.query.all()
        
        total_enrolled = 0
        current_year = date.today().year
        # Define your default admission date
        default_admission_date = date(2024, 7, 1)

        for cls in all_classes:
            try:
                age = int(cls.grade) + 5
            except ValueError:
                age = 20
            
            for i in range(students_per_class):
                # 1. Create Guardian
                last_name = fake.last_name()
                parent = Guardian(
                    father_name=f"{fake.first_name_male()} {last_name}",
                    mother_name=f"{fake.first_name_female()} {last_name}",
                    parent_email=fake.email(),
                    emergency_contact=fake.phone_number()[-10:]
                )
                db.session.add(parent)
                db.session.flush()

                # 2. Create Student
                gender = random.choice([GenderEnum.MALE, GenderEnum.FEMALE])
                first_name = fake.first_name_male() if gender == GenderEnum.MALE else fake.first_name_female()
                
                birth_year = current_year - age
                dob = date(birth_year, random.randint(1, 12), random.randint(1, 28))

                student = Student(
                    admission_no=f"ADM{current_year}{cls.grade}{cls.section}{i:03d}",
                    first_name=first_name,
                    last_name=last_name,
                    dob=dob,
                    gender=gender,
                    guardian_id=parent.id,
                    # ADDED THESE TWO LINES:
                    nationality="Indian",
                    admission_date=default_admission_date
                )
                db.session.add(student)
                db.session.flush()

                # 3. Create Enrollment
                enrollment = Enrollment(
                    student_id=student.id,
                    session_id=session.id,
                    class_id=cls.id,
                    roll_no=i + 1,
                    status="ACTIVE"
                )
                db.session.add(enrollment)
                total_enrolled += 1

        db.session.commit()
        print(f"Successfully seeded {total_enrolled} students with Indian nationality!")

if __name__ == "__main__":
    bulk_seed_students()