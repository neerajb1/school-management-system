import unittest
from app import create_app, db
from app.models.student import Student

class TestStudents(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_students(self):
        with self.app.app_context():
            student = Student(name="John Doe", grade="Grade 10", section="A")
            db.session.add(student)
            db.session.commit()

        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", response.get_data(as_text=True))
