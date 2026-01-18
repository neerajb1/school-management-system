from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://localhost/school-management"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)
