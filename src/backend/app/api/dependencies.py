from typing import Generator
from app.db.sessions import SessionLocal


# Dependency
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()