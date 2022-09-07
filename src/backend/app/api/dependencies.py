from typing import Generator
# from sqlalchemy.ext.asyncio import AsyncSession
from app.db.sessions import SessionLocal, AsyncSessionLocal


# Dependency
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def async_get_db() -> Generator:
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()
