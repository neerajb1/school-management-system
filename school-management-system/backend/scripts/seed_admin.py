from app import create_app, db
from app.models.users import Role, UserAccount


def seed_admin():
    app = create_app()

    with app.app_context():
        print("Seeding admin user...")

        # 1️⃣ Create ADMIN role if not exists
        admin_role = db.session.query(Role).filter_by(name="ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN")
            db.session.add(admin_role)
            db.session.commit()
            print("Created ADMIN role")

        # 2️⃣ Create admin user if not exists
        admin_email = "admin@school.com"

        admin_user = (
            db.session.query(UserAccount)
            .filter_by(email=admin_email)
            .first()
        )

        if not admin_user:
            admin_user = UserAccount(
                email=admin_email,
                password_hash="admin123",  # TEMP (replace later with hash)
                role_id=admin_role.id,
                user_type="ADMIN",
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Created admin user")
        else:
            print("Admin user already exists")

        print("Admin seed complete ✅")


if __name__ == "__main__":
    seed_admin()
