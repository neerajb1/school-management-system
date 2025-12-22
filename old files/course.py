from app import db

# The Association Table (The "Middle-Man")
teacher_courses = db.Table('teacher_courses',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)

class Course(db.Model):
    __tablename__ = 'courses'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # The Relationship
    teachers = db.relationship('Teacher', secondary=teacher_courses, backref='courses')

    def to_dict(self):
        return {
            "id": self.id,
            "course_code": self.course_code,
            "title": self.title,
            "teachers": [f"{t.first_name} {t.last_name}" for t in self.teachers]
        }