from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi import HTTPException, status
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy.sql.expression import exists

from app.db.base_class import Base
# from app.db.sessions import SessionLocal


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
class CRUDBase(Generic[ModelType, CreateSchemaType]):
    
    def __init__(self, model: Type[ModelType]):
        """ CRUD object with default methods to Create, Read, Update, & Delete

        Args:
            model (Type[ModelType]): A SQLAlchemy model class
        """
        self.model = model

    def get(self, *, db: Session, id: int) -> ModelType:
        return db.query(
            self.model
        ).filter(getattr(self.model, "id", None) == id).first()


    def get_multi(
        self,
        *,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """ Get multi items from database without filter criteria

        Args:
            db (AsyncSession): Async db session
            skip (int, optional): Optional Offset. Defaults to 0.
            limit (int, optional): Optional limit. Defaults to 100.

        Returns:
            List[ModelType]: Matching results list
        """
        
        return db.query(self.model).offset(skip).limit(limit).all()


    def create(
        self,
        *,
        db: Session,
        obj_in: CreateSchemaType
    ) -> ModelType:
        """ Try to create item in database

        Args:
            db (AsyncSession): Async db session
            obj_in (CreateSchemaType): Schema to create

        Raises:
            HTTPException: HTTP_400_BAD_REQUEST if item already exists
            HTTPException: HTTP_400_BAD_REQUEST for other errors

        Returns:
            ModelType: Instance of created object
        """

        try:
            # try json encode
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            
            # add to database
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            # return instance
            return db_obj
            
        except IntegrityError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self.model.__name__} already exists. Check parameters"
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somethig was wrong"
            )