from app.models.users import Staff
from app.models.academics import TeacherAssignment
from app import db

class TeacherService:
    @staticmethod
    def add_teacher(data):
        try:
            new_teacher = Staff(
                emp_id=data['employee_id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                department_id=data['department'],
                qualification=data.get('qualification'),
                phone=data.get('phone')
            )
            db.session.add(new_teacher)
            db.session.commit()
            return {"status": "success", "teacher_id": new_teacher.id}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_all_teachers():
        return Staff.query.all()

def get_teacher_by_emp_id(emp_id):
    return Staff.query.filter_by(emp_id=emp_id).first()

def create_teacher(data):
    teacher = Staff(
        emp_id=data["emp_id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
        photo_url=data.get("photo_url"),
        role_id=data["role_id"],
        department_id=data["department_id"]
    )
    db.session.add(teacher)
    db.session.commit()
    return teacher

def get_teacher_assignments(teacher_id):
    return TeacherAssignment.query.filter_by(staff_id=teacher_id).all()