from app import db
from datetime import datetime

class Teacher(db.Model):
    __tablename__ = 'teachers'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(50), nullable=False) # e.g., Mathematics, Science
    qualification = db.Column(db.String(100))
    joining_date = db.Column(db.Date, default=datetime.utcnow().date)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "full_name": f"{self.first_name} {self.last_name}",
            "email": self.email,
            "department": self.department,
            "qualification": self.qualification,
            "is_active": self.is_active
        }