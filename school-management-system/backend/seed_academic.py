import random
from datetime import date, timedelta
from app import app
from app.models.base import db
from app.models.academics import Enrollment, Attendance, Marksheet, Subject

def seed_academic_data():
    with app.app_context():
        enrollments = Enrollment.query.all()
        subjects = Subject.query.all()
        
        if not subjects:
            print("Error: No subjects found. Seed subjects first.")
            return

        for enrollment in enrollments:
            # Seed 30 days of attendance
            for i in range(30):
                record = Attendance(
                    enrollment_id=enrollment.id,
                    date=date.today() - timedelta(days=i),
                    status=random.choice(["PRESENT", "PRESENT", "ABSENT"])
                )
                db.session.add(record)

            # Seed marks for every subject (matching your screenshot format)
            for subject in subjects:
                mark = Marksheet(
                    enrollment_id=enrollment.id,
                    subject_id=subject.id,
                    marks_obtained=random.uniform(50.0, 98.0),
                    total_marks=100.0
                )
                db.session.add(mark)
        
        db.session.commit()
        print("Academic data successfully seeded!")

if __name__ == "__main__":
    seed_academic_data()