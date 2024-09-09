from typing import Any, Generic, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import exc
from sqlmodel import Session, SQLModel, func, select
from sqlmodel.sql.expression import Select

from app.api.deps import get_db

ModelType = TypeVar("ModelType", bound=SQLModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.session = next(get_db())

    def get_one_by_id(
        self,
        *,
        id: int | str,
        session: Session | None = None,
        filters: list[Any] | None = None,
    ) -> ModelType | None:
        session = session or self.session
        if filters:
            query = select(self.model).filter(self.model.__table__.primary_key.columns[0] == id, *filters)
        else:
            query = select(self.model).where(self.model.__table__.primary_key.columns[0] == id)
        response = session.execute(query)
        return response.scalar_one_or_none()

    def get_many_by_ids(
        self,
        *,
        list_ids: list[int | str],
        filters: list[Any] | None = None,
        session: Session | None = None,
    ) -> list[ModelType] | None:
        session = session or self.session
        if filters:
            query = select(self.model).filter(self.model.__table__.primary_key.columns[0].in_(list_ids), *filters)
        else:
            query = select(self.model).where(self.model.__table__.primary_key.columns[0].in_(list_ids))
        response = session.execute(
            query
        )
        return response.scalars().all()

    def get_count(
        self, session: Session | None = None
    ) -> ModelType | None:
        session = session or self.session
        response = session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    def get_list(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: T | Select[T] | None = None,
        filters: list[Any] | None = None,
        order: str | None = None,  # asc or desc
        order_by: tuple | None = None,  # Field name
        session: Session | None = None,
    ) -> list[ModelType]:
        session = session or self.session
        if query is None:
            query = select(self.model).offset(skip).limit(limit)
        if filters:
            query = query.filter(*filters)
        if order_by:
            columns = self.model.__table__.columns
            if order == 'asc':
                query = query.order_by(columns[order_by].asc())
            else:
                query = query.order_by(columns[order_by].desc())
        response = session.execute(query)
        return response.scalars().all()


    def create(
        self,
        *,
        obj_in: ModelType,
        created_by_id: int | str | None = None,
        session: Session | None = None,
    ) -> ModelType:
        db_session = session or self.session
        db_obj = self.model.model_validate(obj_in)  # type: ignore

        if created_by_id:
            db_obj.created_by_id = created_by_id

        try:
            db_session.add(db_obj)
            db_session.commit()
        except exc.IntegrityError as e:
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"{e}",
            )
        db_session.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: dict[str, Any] | ModelType,
        session: Session | None = None,
    ) -> ModelType:
        db_session = session or self.session

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        db_session.commit()
        db_session.refresh(obj_current)
        return obj_current

    def remove(
        self, *, id: int | str, session: Session | None = None
    ) -> ModelType:
        db_session = session or self.session
        response = db_session.execute(
            select(self.model).where(self.model.__table__.primary_key.columns[0] == id)
        )
        obj = response.scalar_one()
        db_session.delete(obj)
        db_session.commit()
        return obj
