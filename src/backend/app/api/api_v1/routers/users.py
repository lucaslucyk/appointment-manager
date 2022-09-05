
from typing import List
from app.schemas import User
from fastapi import APIRouter

router = APIRouter(include_in_schema=True)

users = [User(
    email="asd@asd.com",
    password="secret",
    is_active=True,
    first_name="Lucas",
    last_name="Lucyk",
    is_professional=True
)]

@router.get("/")
async def get_users() -> List[User]:
    return users