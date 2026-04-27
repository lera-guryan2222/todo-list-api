import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

IS_TESTING = os.getenv("TESTING", "False").lower() == "true"
IS_CI = os.getenv("CI", "False").lower() == "true"

if IS_TESTING or IS_CI:
    DATABASE_URL = "sqlite:///:memory:?check_same_thread=False"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://todo_user:todo_password@postgres:5432/todo_db"
    )
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
