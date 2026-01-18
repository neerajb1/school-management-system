from datetime import date, datetime, timedelta
import random

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models import (
    # base / enums
    GenderEnum,
    FeeFrequencyEnum,
    PaymentMethodEnum,

    # users
    School,
    Role,
    Department,
    Staff,
    Guardian,
    Student,
    UserAccount,
    Transport,
    MedicalRecord,
    Announcement,

    # academics
    AcademicSession,
    ClassRoom,
    Subject,
    Enrollment,
    Attendance,
    Exam,
    Marksheet,
    TeacherAssignment,
    GradeScale,

    # finance
    FeeType,
    FeeMaster,
    DiscountOffer,
    StudentLedger,
    FeeInstallment,
    Transaction,
)


def reset_db(session):
    """
    Delete data in FK-safe order (children → parents)
    """
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


def seed():
    session = SessionLocal()

    try:
        print("Resetting database...")
        reset_db(session)

        print("Seeding school...")
        school = School(
            name="Green Valley Public School",
            address="Main Road, City Center",
            contact_number="9999999999",
            registration_no="SCH-REG-001",
            logo_url="https://school/logo.png",
        )
        session.add(school)

        print("Seeding roles...")
        roles = [Role(name=r) for r in ["ADMIN", "TEACHER", "STUDENT", "PARENT", "ACCOUNTANT"]]
        session.add_all(roles)

        print("Seeding departments...")
        departments = [Department(name=n) for n in ["Science", "Maths", "Arts", "Sports", "Administration"]]
        session.add_all(departments)

        print("Seeding academic session...")
        session_2025 = AcademicSession(
            name="2025-2026",
            start_date=date(2025, 4, 1),
            end_date=date(2026, 3, 31),
            is_active=True,
        )
        session.add(session_2025)

        print("Seeding classes...")
        classes = [
            ClassRoom(name=f"Class {i}", section=s)
            for i in range(1, 6)
            for s in ["A", "B"]
        ]
        session.add_all(classes)

        print("Seeding subjects...")
        subjects = [
            Subject(name=n, code=n[:3].upper())
            for n in ["Mathematics", "Science", "English", "History", "Geography"]
        ]
        session.add_all(subjects)

        print("Seeding staff...")
        staff_list = []
        for i in range(10):
            staff = Staff(
                emp_id=f"EMP{i+1:03}",
                first_name=f"Teacher{i}",
                email=f"teacher{i}@school.com",
                role=roles[1],
                department=random.choice(departments),
                joining_date=date(2020, 6, 1),
            )
            staff_list.append(staff)
        session.add_all(staff_list)

        print("Seeding guardians & students...")
        students = []
        for i in range(10):
            guardian = Guardian(
                father_name=f"Father{i}",
                parent_email=f"parent{i}@mail.com",
                emergency_contact="8888888888",
            )
            student = Student(
                admission_no=f"ADM{i+1:04}",
                first_name=f"Student{i}",
                gender=random.choice(list(GenderEnum)),
                admission_date=date(2024, 6, 1),
                guardian=guardian,
            )
            students.append(student)
            session.add_all([guardian, student])

        print("Seeding enrollments...")
        enrollments = []
        for student in students:
            enrollments.append(
                Enrollment(
                    student=student,
                    class_room=random.choice(classes),
                    session=session_2025,
                    roll_no=str(random.randint(1, 50)),
                )
            )
        session.add_all(enrollments)

        print("Seeding attendance...")
        for enrollment in enrollments:
            for d in range(10):
                session.add(
                    Attendance(
                        enrollment=enrollment,
                        date=date.today() - timedelta(days=d),
                        is_present=random.choice([True, False]),
                    )
                )

        print("Seeding exams & marksheets...")
        exam = Exam(name="Mid Term", session=session_2025)
        session.add(exam)

        for enrollment in enrollments:
            for subject in subjects:
                session.add(
                    Marksheet(
                        enrollment=enrollment,
                        subject=subject,
                        exam=exam,
                        marks_obtained=random.randint(40, 95),
                        max_marks=100,
                        grade="A",
                    )
                )

        print("Seeding grade scale...")
        grades = [
            ("A", 90, 100),
            ("B", 75, 89),
            ("C", 60, 74),
            ("D", 40, 59),
        ]
        for g, min_p, max_p in grades:
            session.add(
                GradeScale(
                    grade_name=g,
                    min_percentage=min_p,
                    max_percentage=max_p,
                    grade_point=4.0,
                )
            )

        print("Seeding fee types & masters...")
        fee_types = [
            FeeType(name="Tuition Fee", frequency=FeeFrequencyEnum.MONTHLY),
            FeeType(name="Library Fee", frequency=FeeFrequencyEnum.YEARLY),
        ]
        session.add_all(fee_types)

        fee_masters = []
        for cls in classes:
            fee_masters.append(
                FeeMaster(
                    class_room=cls,
                    session=session_2025,
                    fee_type=fee_types[0],
                    amount=2000,
                )
            )
        session.add_all(fee_masters)

        print("Seeding discounts, ledger, installments & transactions...")
        discount = DiscountOffer(
            name="Sibling Discount",
            discount_percentage=10,
            is_active=True,
        )
        session.add(discount)

        for enrollment in enrollments:
            ledger = StudentLedger(
                enrollment=enrollment,
                fee_master=random.choice(fee_masters),
                original_amount=2000,
                discount_offer=discount,
                discount_amount=200,
                final_amount=1800,
            )
            session.add(ledger)

            installment = FeeInstallment(
                ledger=ledger,
                installment_no=1,
                amount=1800,
                is_paid=True,
            )
            session.add(installment)

            session.add(
                Transaction(
                    installment=installment,
                    payment_date=datetime.utcnow(),
                    amount_paid=1800,
                    payment_method=PaymentMethodEnum.UPI,
                )
            )

        print("Seeding announcements...")
        for i in range(10):
            session.add(
                Announcement(
                    title=f"Notice {i}",
                    content="School will remain open.",
                    target_audience="ALL",
                    expiry_date=date.today() + timedelta(days=30),
                )
            )

        session.commit()
        print("✅ Database seeded successfully.")

    except IntegrityError as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    seed()
