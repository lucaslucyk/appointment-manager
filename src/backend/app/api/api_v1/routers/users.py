
from typing import List
from app import crud
from app.schemas import User
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import dependencies as deps

from app.schemas.users import User, UserCreate

router = APIRouter(include_in_schema=True)


@router.get("/")
async def get_users(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
) -> List[User]:
    
    return await crud.user.get_multi(db=db)


@router.get("/{id}")
async def get_user(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
    id: int = Path()
) -> User:
    
    return await crud.user.get_or_404(db=db, id=id)


@router.post("/")
async def create_user(
    *,
    db: AsyncSession = Depends(deps.async_get_db),
    user: UserCreate
) -> List[User]:
    
    # return users
    # return crud.user.create(db=db, obj_in=user)
    return await crud.user.create(db=db, obj_in=user)