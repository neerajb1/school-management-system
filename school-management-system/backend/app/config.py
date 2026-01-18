import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://neeraj@localhost/school-management"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask secret
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # JWT secret (THIS WAS MISSING)
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-secret-key-change-this"
    )
