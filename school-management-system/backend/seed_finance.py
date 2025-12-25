from decimal import Decimal
from app import db, create_app
from app.models.finance import FeeType, FeeMaster, StudentLedger
from app.models.academics import ClassRoom, Enrollment, AcademicSession
from app.models.base import FeeFrequencyEnum

app = create_app()

def seed_finance():
    with app.app_context():
        print("Starting Finance Seeding...")
        
        session = AcademicSession.query.filter_by(is_current=True).first()
        if not session:
            print("No active session found!")
            return

        # 1. Create Fee Types
        tuition_type = FeeType.query.filter_by(name="Tuition Fee").first()
        if not tuition_type:
            tuition_type = FeeType(name="Tuition Fee", frequency=FeeFrequencyEnum.MONTHLY)
            db.session.add(tuition_type)
        
        admission_type = FeeType.query.filter_by(name="Admission Fee").first()
        if not admission_type:
            admission_type = FeeType(name="Admission Fee", frequency=FeeFrequencyEnum.ONETIME)
            db.session.add(admission_type)
        
        db.session.flush()

        # 2. Create Fee Master (Pricing per Class)
        print("Setting up Fee Masters (Pricing)...")
        classes = ClassRoom.query.all()
        for cls in classes:
            # Logic: Higher grades pay more. Science stream pays extra for labs.
            try:
                grade_num = int(cls.grade)
                base_amt = 2000 + (grade_num * 200) # Grade 1: 2200, Grade 12: 4400
            except ValueError:
                base_amt = 5000 # Default for Higher Ed
            
            if cls.stream == "Science":
                base_amt += 500 # Lab Fees
            
            # Check if Master already exists for this class/session
            master = FeeMaster.query.filter_by(
                fee_type_id=tuition_type.id, 
                class_id=cls.id, 
                session_id=session.id
            ).first()

            if not master:
                master = FeeMaster(
                    fee_type_id=tuition_type.id,
                    class_id=cls.id,
                    session_id=session.id,
                    amount=Decimal(base_amt)
                )
                db.session.add(master)
        
        db.session.commit()

        # 3. Generate Ledgers (The Invoices for Students)
        print("Generating Student Ledgers (Billing)...")
        enrollments = Enrollment.query.filter_by(session_id=session.id).all()
        
        for enroll in enrollments:
            # Find the tuition fee master for this student's class
            master = FeeMaster.query.filter_by(
                class_id=enroll.class_id, 
                session_id=session.id,
                fee_type_id=tuition_type.id
            ).first()

            if master:
                # Create a ledger entry (billing the student)
                # Check if already billed to avoid duplicates
                existing_ledger = StudentLedger.query.filter_by(
                    enrollment_id=enroll.id,
                    fee_master_id=master.id
                ).first()

                if not existing_ledger:
                    ledger = StudentLedger(
                        enrollment_id=enroll.id,
                        fee_master_id=master.id,
                        discount_amount=Decimal(0),
                        final_amount=master.amount,
                        status="UNPAID" # Initial status
                    )
                    db.session.add(ledger)
        
        db.session.commit()
        print(f"Finance Setup Complete! {len(enrollments)} students have been billed.")

if __name__ == "__main__":
    seed_finance()