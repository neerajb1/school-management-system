from app import db, create_app
from app.models.academics import Subject, ClassRoom, TeacherAssignment, AcademicSession
from app.models.users import Staff

app = create_app()

def seed_subjects_and_assignments():
    with app.app_context():
        print("Seeding Indian Standard Subjects...")
        
        # Define Subjects
        subject_data = [
            {"name": "English", "code": "ENG"},
            {"name": "Hindi", "code": "HIN"},
            {"name": "Mathematics", "code": "MATH"},
            {"name": "Science", "code": "SCI"},
            {"name": "Social Science", "code": "SST"},
            {"name": "Physics", "code": "PHY"},
            {"name": "Chemistry", "code": "CHEM"},
            {"name": "Biology", "code": "BIO"},
            {"name": "History", "code": "HIST"},
            {"name": "Geography", "code": "GEO"},
            {"name": "Political Science", "code": "POL"}
        ]

        # Get or Create Subjects
        for data in subject_data:
            if not Subject.query.filter_by(code=data['code']).first():
                db.session.add(Subject(**data))
        db.session.commit()

        # Assign Subjects to Classes
        session = AcademicSession.query.filter_by(is_current=True).first()
        teacher = Staff.query.first() # Assigning our first teacher to all for now
        all_classes = ClassRoom.query.all()

        for cls in all_classes:
            # Determine which subject codes to assign
            codes = ["ENG", "HIN"] # Base subjects for everyone
            
            try:
                grade_num = int(cls.grade)
                if grade_num <= 10:
                    codes += ["MATH", "SCI", "SST"]
                elif cls.stream == "Science":
                    codes += ["PHY", "CHEM", "MATH"]
                elif cls.stream == "Arts":
                    codes += ["HIST", "GEO", "POL"]
            except ValueError:
                # Handle BA/MA or non-numeric grades
                if "BA" in cls.grade: codes += ["HIST", "POL"]
                if "B.Sc" in cls.grade: codes += ["PHY", "CHEM"]

            for code in codes:
                sub = Subject.query.filter_by(code=code).first()
                # Create Assignment
                if not TeacherAssignment.query.filter_by(
                    class_id=cls.id, subject_id=sub.id, session_id=session.id
                ).first():
                    assignment = TeacherAssignment(
                        staff_id=teacher.id,
                        class_id=cls.id,
                        subject_id=sub.id,
                        session_id=session.id
                    )
                    db.session.add(assignment)
        
        db.session.commit()
        print("Academic assignments complete!")

if __name__ == "__main__":
    seed_subjects_and_assignments()