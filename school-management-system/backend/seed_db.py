from app import db, create_app
from app.models.academics import AcademicSession, ClassRoom
from app.models.users import Role, Department

app = create_app()

def seed_production_structure():
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("Setting up School Infrastructure (Indian Standard)...")
        session = AcademicSession(year_label="2024-2025", is_current=True)
        db.session.add(session)

        # 1. Loop through Grades 1 to 12
        for g in range(1, 13):
            for s in ['A', 'B']:
                # Logic: Below 9 is General. 9-12 can be Science/Arts/Commerce
                if g < 9:
                    db.session.add(ClassRoom(grade=str(g), section=s, stream="General"))
                else:
                    # For 9-12, usually schools have specific sections for specific streams
                    # Let's say Section A is Science and Section B is Arts
                    stream_name = "Science" if s == 'A' else "Arts"
                    db.session.add(ClassRoom(grade=str(g), section=s, stream=stream_name))



        # 3. Setup Departments (For Staff/Teachers)
        # In India, we use 'Primary', 'Middle', and then Subject-specific depts
        depts = ["General Education", "Science", "Arts", "Commerce", "Administration"]
        for name in depts:
            db.session.add(Department(name=name))

        db.session.commit()
        print("Success: Seeded 1-8 (General) and 9-12 + Higher Ed (Stream-based)!")

if __name__ == "__main__":
    seed_production_structure()