from seed_db import seed_production_structure # Your Phase 1
from seed_data import seed_production_data      # Your Phase 2 (Initial Staff)
from seed_bulk_students import bulk_seed_students # The Bulk Script
from seed_subject import seed_subjects_and_assignments # Subjects & Assignments

if __name__ == "__main__":
    print("--- STARTING FULL DATABASE SEED ---")
    seed_production_structure()
    seed_production_data()
    bulk_seed_students(students_per_class=10) # 10 per class = 240 students
    seed_subjects_and_assignments()
    print("--- SCHOOL IS NOW FULLY OPERATIONAL ---")