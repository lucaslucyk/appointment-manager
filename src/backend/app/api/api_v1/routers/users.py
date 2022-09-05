
from typing import List
from app import crud
from app.schemas import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import dependencies as deps

from app.schemas.users import User, UserCreate

router = APIRouter(include_in_schema=True)

# users = [User(
#     email="asd@asd.com",
#     password="secret",
#     is_active=True,
#     first_name="Lucas",
#     last_name="Lucyk",
#     is_professional=True
# )]

@router.get("/")
async def get_users(
    db: Session = Depends(deps.get_db)
) -> List[User]:
    
    # return users
    return crud.user.get_multi(db=db)


@router.post("/")
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user: UserCreate
) -> List[User]:
    
    # return users
    return crud.user.create(db=db, obj_in=user)