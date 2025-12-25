from app.models.academics import Subject, ClassRoom
from app.models.users import Staff  # Updated import
from app import db

class CourseService:
    @staticmethod
    def create_course(data):
        try:
            new_course = Subject(
                name=data['name'],
                code=data['code']
            )
            db.session.add(new_course)
            db.session.commit()
            return {"status": "success", "course_id": new_course.id}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}

    @staticmethod
    def assign_teacher(class_id, subject_id, staff_id):
        try:
            class_room = ClassRoom.query.get(class_id)
            subject = Subject.query.get(subject_id)
            staff = Staff.query.get(staff_id)
            if not class_room or not subject or not staff:
                return {"status": "error", "message": "Class, Subject, or Staff not found"}
            
            # Logic to assign teacher (if needed, you can add TeacherAssignment logic here)
            return {"status": "success", "message": f"Assigned {staff.first_name} to {subject.name} in {class_room.grade}-{class_room.section}"}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}

def get_all_subjects():
    return Subject.query.all()

def create_subject(data):
    subject = Subject(
        name=data["name"],
        code=data["code"]
    )
    db.session.add(subject)
    db.session.commit()
    return subject

def get_all_classes():
    return ClassRoom.query.all()

def create_class(data):
    class_room = ClassRoom(
        grade=data["grade"],
        section=data["section"]
    )
    db.session.add(class_room)
    db.session.commit()
    return class_room