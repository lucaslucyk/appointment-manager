from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union
)
from fastapi import HTTPException, status
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    
    def __init__(self, model: Type[ModelType]):
        """ CRUD object with default methods to Create, Read, Update, & Delete

        Args:
            model (Type[ModelType]): A SQLAlchemy model class
        """
        self.model = model


    async def get(self, *, db: AsyncSession, id: int)-> ModelType:
        """ Get row from model where id == model.id

        Args:
            db (AsyncSession): Async db session
            id (Any): Id to filter

        Returns:
            Optional[ModelType]: ModelType instance or None if id not exists
        """
        result = await db.execute(
            select(self.model)
            .where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    
    async def get_or_404(
        self,
        db: AsyncSession,
        id: Any
    ) -> Optional[ModelType]:
        """ Try to dgt row from model where id == model.id

        Args:
            db (AsyncSession): Async db session
            id (Any): Id to filter

        Raises:
            HTTPException: HTTP_404_NOT_FOUND if item does not exist

        Returns:
            Optional[ModelType]: ModelType instance
        """
        # try get item
        obj = await self.get(db=db, id=id)
        
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} with id {id} does not exist"
            )

        return obj

    
    async def exists(self, db: AsyncSession, **kwargs) -> bool:
        """ Check if an item exists in database. Use kwargs to filter elements

        Args:
            db (AsyncSession): Async db Session

        Returns:
            bool: True if item found, False if not.
        """
        result = await db.execute(
            select(self.model)
            .filter_by(**kwargs)
            .limit(1)
        )
        return bool(result.scalar_one_or_none())


    async def get_multi(
        self,
        *,
        db: AsyncSession,
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
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    
    async def filter_by(
        self,
        *,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        multiple: bool = True,
        **kwargs
    ) -> Union[List[ModelType], ModelType]:
        """ Get items from database using kwargs to filter

        Args:
            db (AsyncSession): Async db session
            skip (int, optional): Optional Offset. Defaults to 0.
            limit (int, optional): Optional limit. Defaults to 100.
            multiple (bool, optional): 
                Optional bool to get single or multi items.
                Defaults to True.

        Returns:
            Union[List[ModelType], ModelType]: 
                Instance or list of intance of matching items.
        """
        # try to get
        result = await db.execute(
            select(self.model)
            .filter_by(**kwargs)
            .offset(skip)
            .limit(limit)
        )

        # all if multiple
        if multiple:
            return result.scalars().all()

        # else, first only
        return result.scalar_one_or_none()


    async def filter(
        self,
        *,
        db: AsyncSession,
        filters: Union[list, tuple],
        criterion: Callable = and_,
        skip: int = 0,
        limit: int = 100,
        multiple: bool = True
    ) -> Union[List[ModelType], ModelType]:
        """ Get items from database using `filters` to filter

        Args:
            db (AsyncSession): Async db session
            filters (Union[list, tuple]): Filters iterable.
            criterion (Callable, optional):
                Criterion to filter.
                Defaults to sqlalchemy.and_.
            skip (int, optional): Optional Offset. Defaults to 0.
            limit (int, optional): Optional limit. Defaults to 100.
            multiple (bool, optional): 
                Optional bool to get single or multi items.
                Defaults to True.

        Returns:
            Union[List[ModelType], ModelType]: 
                Instance or list of intance of matching items.
        """
        
        # try to get
        result = await db.execute(
            select(self.model)
            .where(criterion(*filters))
            .offset(skip)
            .limit(limit)
        )

        # all if multiple
        if multiple:
            return result.scalars().all()

        # else, first only
        return result.scalar_one_or_none()

    
    async def create(
        self,
        *,
        db: AsyncSession,
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
            
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

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


    async def update(
        self,
        *,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """ Update a database item with an update schema

        Args:
            db (AsyncSession): Async db session
            db_obj (ModelType): Item to update
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): 
                New partial or full data for database item

        Returns:
            ModelType: [description]
        """
        
        # obj_in to dict
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # update db_obj with each field of obj_in
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # save, commit and refresh session
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        # return updated object
        return db_obj


    async def delete(self, *, db: AsyncSession, id: int) -> ModelType:
        """ Delete an item from database

        Args:
            db (AsyncSession): Async db session
            id (int): Id of model to delete

        Returns:
            ModelType: Deleted object instance
        """
        
        obj = await self.get_or_404(db=db, id=id)

        await db.delete(obj)
        await db.commit()

        return obj