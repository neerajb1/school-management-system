from app import create_app
from app import db

# import ALL models explicitly
from app.models import users, academics, finance

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("Done.")
