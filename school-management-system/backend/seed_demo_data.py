from datetime import date, datetime, timedelta
import random

from sqlalchemy import delete
from app.db.session import SessionLocal

from app.models import (
    GenderEnum,
    FeeFrequencyEnum,
    PaymentMethodEnum,

    School, Role, Department, Staff, Guardian, Student,
    UserAccount, Transport, MedicalRecord, Announcement,

    AcademicSession, ClassRoom, Subject, Enrollment,
    Attendance, Exam, Marksheet, TeacherAssignment, GradeScale,

    FeeType, FeeMaster, DiscountOffer, StudentLedger,
    FeeInstallment, Transaction,
)


# -------------------------
# CLEAN DB (SAFE ORDER)
# -------------------------
def reset_db(session):
    tables = [
        Transaction,
        FeeInstallment,
        StudentLedger,
        DiscountOffer,
        FeeMaster,
        FeeType,

        Marksheet,
        Attendance,
        Exam,
        TeacherAssignment,
        Enrollment,
        GradeScale,
        Subject,
        ClassRoom,
        AcademicSession,

        Transport,
        MedicalRecord,
        Student,
        Guardian,
        Staff,
        Department,
        Role,
        UserAccount,
        Announcement,
        School,
    ]

    for table in tables:
        session.execute(delete(table))
    session.commit()


# -------------------------
# DEMO DATA
# -------------------------
STUDENT_NAMES = [
    ("Aarav", "Sharma", GenderEnum.MALE),
    ("Ananya", "Verma", GenderEnum.FEMALE),
    ("Rohan", "Mehta", GenderEnum.MALE),
    ("Isha", "Patel", GenderEnum.FEMALE),
    ("Kabir", "Singh", GenderEnum.MALE),
    ("Diya", "Gupta", GenderEnum.FEMALE),
    ("Arjun", "Malhotra", GenderEnum.MALE),
    ("Sneha", "Iyer", GenderEnum.FEMALE),
    ("Yash", "Agarwal", GenderEnum.MALE),
    ("Pooja", "Nair", GenderEnum.FEMALE),
]

TEACHERS = [
    ("Neha", "Gupta", "Mathematics"),
    ("Suresh", "Iyer", "Science"),
    ("Pooja", "Nair", "English"),
    ("Amit", "Sharma", "History"),
    ("Kavita", "Joshi", "Geography"),
]

SUBJECT_MAP = {
    "Mathematics": "MATH",
    "Science": "SCI",
    "English": "ENG",
    "History": "HIS",
    "Geography": "GEO",
}


def seed():
    session = SessionLocal()

    print("🔄 Resetting database")
    reset_db(session)

    # -------------------------
    # SCHOOL
    # -------------------------
    school = School(
        name="Green Valley Public School",
        address="Sector 12, New Delhi",
        contact_number="011-45678900",
        registration_no="GVPS-DEL-2008",
    )
    session.add(school)

    # -------------------------
    # ROLES & DEPARTMENTS
    # -------------------------
    roles = {
        r.name: r for r in [
            Role(name="ADMIN"),
            Role(name="TEACHER"),
            Role(name="STUDENT"),
            Role(name="PARENT"),
            Role(name="ACCOUNTANT"),
        ]
    }
    session.add_all(roles.values())

    departments = {}
    for name in SUBJECT_MAP.keys():
        dept = Department(name=name)
        departments[name] = dept
        session.add(dept)

    # -------------------------
    # ACADEMIC SESSION
    # -------------------------
    session_2025 = AcademicSession(
        name="2025-2026",
        start_date=date(2025, 4, 1),
        end_date=date(2026, 3, 31),
        is_active=True,
    )
    session.add(session_2025)

    # -------------------------
    # CLASSES
    # -------------------------
    classes = []
    for grade in range(1, 6):
        for section in ["A", "B"]:
            cls = ClassRoom(name=f"Class {grade}", section=section)
            classes.append(cls)
            session.add(cls)

    # -------------------------
    # SUBJECTS
    # -------------------------
    subjects = {}
    for name, code in SUBJECT_MAP.items():
        sub = Subject(name=name, code=code)
        subjects[name] = sub
        session.add(sub)

    # -------------------------
    # STAFF (TEACHERS)
    # -------------------------
    staff_members = []
    for idx, (fname, lname, dept_name) in enumerate(TEACHERS, start=1):
        staff = Staff(
            emp_id=f"TCH{idx:03}",
            first_name=fname,
            last_name=lname,
            email=f"{fname.lower()}@gvps.edu.in",
            role=roles["TEACHER"],
            department=departments[dept_name],
            joining_date=date(2018, 6, 1),
            qualification="B.Ed, M.Ed",
        )
        staff_members.append(staff)
        session.add(staff)

    # -------------------------
    # GUARDIANS & STUDENTS
    # -------------------------
    students = []
    for idx, (fname, lname, gender) in enumerate(STUDENT_NAMES, start=1):
        guardian = Guardian(
            father_name=f"Mr. {lname}",
            parent_email=f"{lname.lower()}@gmail.com",
            emergency_contact="98" + str(random.randint(10000000, 99999999)),
        )
        student = Student(
            admission_no=f"GVPS-{2025}-{idx:03}",
            first_name=fname,
            last_name=lname,
            gender=gender,
            dob=date(2015, 6, 15),
            admission_date=date(2024, 6, 1),
            guardian=guardian,
        )
        students.append(student)
        session.add_all([guardian, student])

    # -------------------------
    # ENROLLMENTS
    # -------------------------
    enrollments = []
    for student in students:
        cls = random.choice(classes)
        enroll = Enrollment(
            student=student,
            class_room=cls,
            session=session_2025,
            roll_no=str(random.randint(1, 40)),
        )
        enrollments.append(enroll)
        session.add(enroll)

    # -------------------------
    # ATTENDANCE
    # -------------------------
    for enroll in enrollments:
        for i in range(10):
            session.add(
                Attendance(
                    enrollment=enroll,
                    date=date.today() - timedelta(days=i),
                    is_present=random.choice([True, True, True, False]),
                )
            )

    # -------------------------
    # EXAMS & MARKS
    # -------------------------
    exam = Exam(name="Mid Term Examination", session=session_2025)
    session.add(exam)

    for enroll in enrollments:
        for sub in subjects.values():
            session.add(
                Marksheet(
                    enrollment=enroll,
                    subject=sub,
                    exam=exam,
                    marks_obtained=random.randint(55, 95),
                    max_marks=100,
                    grade=random.choice(["A", "B", "C"]),
                )
            )

    # -------------------------
    # GRADE SCALE
    # -------------------------
    for grade, min_p, max_p in [
        ("A", 90, 100),
        ("B", 75, 89),
        ("C", 60, 74),
        ("D", 40, 59),
    ]:
        session.add(
            GradeScale(
                grade_name=grade,
                min_percentage=min_p,
                max_percentage=max_p,
                grade_point=4.0,
            )
        )

    # -------------------------
    # FINANCE
    # -------------------------
    tuition_fee = FeeType(
        name="Tuition Fee",
        frequency=FeeFrequencyEnum.MONTHLY,
    )
    library_fee = FeeType(
        name="Library Fee",
        frequency=FeeFrequencyEnum.YEARLY,
    )
    session.add_all([tuition_fee, library_fee])

    fee_masters = []
    for cls in classes:
        fee_masters.append(
            FeeMaster(
                class_room=cls,
                session=session_2025,
                fee_type=tuition_fee,
                amount=2500,
            )
        )
    session.add_all(fee_masters)

    sibling_discount = DiscountOffer(
        name="Sibling Discount",
        discount_percentage=10,
        is_active=True,
    )
    session.add(sibling_discount)

    for enroll in enrollments:
        ledger = StudentLedger(
            enrollment=enroll,
            fee_master=random.choice(fee_masters),
            original_amount=2500,
            discount_offer=sibling_discount,
            discount_amount=250,
            final_amount=2250,
        )
        session.add(ledger)

        installment = FeeInstallment(
            ledger=ledger,
            installment_no=1,
            amount=2250,
            is_paid=True,
        )
        session.add(installment)

        session.add(
            Transaction(
                installment=installment,
                payment_date=datetime.utcnow(),
                amount_paid=2250,
                payment_method=PaymentMethodEnum.UPI,
            )
        )

    # -------------------------
    # ANNOUNCEMENTS
    # -------------------------
    for i in range(10):
        session.add(
            Announcement(
                title=f"Important Notice {i+1}",
                content="School will remain open as per schedule.",
                target_audience="ALL",
                expiry_date=date.today() + timedelta(days=30),
            )
        )

    session.commit()
    session.close()
    print("✅ Demo-grade data seeded successfully")


if __name__ == "__main__":
    seed()
