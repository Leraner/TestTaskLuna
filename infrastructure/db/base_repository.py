from abc import ABC
from typing import Generic, TypeVar, Any, Type

from sqlalchemy import Result, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.orm import BaseDBModel
from infrastructure.db.specifications import Specification, QueryType
from infrastructure.exceptions.exceptions import DatabaseError
from src.shared_kernel.entities import EntityType

T = TypeVar("T", bound=BaseDBModel)


class BaseRepository(ABC, Generic[T]):
    """
    Base class for all repositories
    """

    def __init__(self, db_session: AsyncSession):
        """
        Args:
            db_session: SQLAlchemy async session
        """
        self._session = db_session

    async def _get_one_by_specs(
        self,
        model: Type[T],
        specs: list[Specification[T]],
    ) -> EntityType | None:
        query = select(model)
        query = self.__apply_specs(
            model=model,
            query=query,
            specs=specs,
        )

        result = await self._execute(query=query)
        result_model = result.scalars().unique().one_or_none()
        return result_model.to_entity() if result_model else None

    async def _get_many_by_specs(
        self,
        model: Type[T],
        specs: list[Specification[T]],
    ) -> list[EntityType]:
        query = select(model)
        query = self.__apply_specs(
            model=model,
            query=query,
            specs=specs,
        )

        result = await self._execute(query=query)
        result_models = result.scalars().unique().all()
        return [result_model.to_entity() for result_model in result_models]

    async def _get_total_count_with_specs(
        self,
        model: Type[T],
        specs: list[Specification[T]],
    ) -> int:
        query = select(func.count(model.id))
        query = self.__apply_specs(
            model=model,
            query=query,
            specs=specs,
        )
        result = await self._execute(query=query)
        return result.scalar_one()

    def __apply_specs(
        self,
        query: QueryType,
        model: Type[T],
        specs: list[Specification[T]],
    ) -> QueryType:
        for spec in specs:
            query = spec.apply(
                query=query,
                model=model,
            )
        return query

    async def _execute(
        self,
        query: QueryType,
    ) -> Result[Any]:
        try:
            result = await self._session.execute(query)
        except IntegrityError as err:
            raise DatabaseError(
                detail="Database query execution failed",
                ru_detail="Ошибка при выполнении запроса к базе данных",
                original_error=err,
            )
        return result

    async def _save_all(self, objects: list[T]) -> None:
        await self.__save_without_refresh(objects=objects)

    async def _save_all_with_return(self, objects: list[T]) -> list[EntityType]:
        await self.__save_with_refresh(objects=objects)
        return [obj.to_entity() for obj in objects]

    async def _save(self, obj: T) -> None:
        await self.__save_without_refresh(objects=[obj])

    async def _save_with_return(self, obj: T) -> EntityType:
        await self.__save_with_refresh(objects=[obj])
        return obj.to_entity()

    async def __save_without_refresh(self, objects: list[T]) -> None:
        for obj in objects:
            self._session.add(obj)

        try:
            await self._session.commit()
        except IntegrityError as err:
            raise DatabaseError(
                detail="Database query execution failed",
                ru_detail="Ошибка при выполнении запроса к базе данных",
                original_error=err,
            )

    async def __save_with_refresh(self, objects: list[T]) -> None:
        for obj in objects:
            self._session.add(obj)

        try:
            await self._session.flush()

            for obj in objects:
                await self._session.refresh(obj)

            await self._session.commit()
        except IntegrityError as err:
            raise DatabaseError(
                detail="Database query execution failed",
                ru_detail="Ошибка при выполнении запроса к базе данных",
                original_error=err,
            )

    async def _delete(self, obj: T) -> None:
        await self._session.delete(obj)

        try:
            await self._session.commit()
        except IntegrityError as err:
            raise DatabaseError(
                detail="Database query execution failed",
                ru_detail="Ошибка при выполнении запроса к базе данных",
                original_error=err,
            )
