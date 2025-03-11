from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import ColumnExpressionArgument, Result, Select, select
from dal.models._base import Common
from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

class SQLAlchemyRepository():
    Model: type[Common]
    
    def __init__(self, Model: type[Common]) -> None:
        self.Model = Model
        
    async def create(self, session: AsyncSession, author_id: UUID, **data) -> Common:
        entity = self.Model(**data)
        entity.created_at = datetime.now()
        entity.created_by = author_id
        entity.modified_at = datetime.now()
        entity.modified_by = author_id
        session.add(instance=entity)
        return entity
        
    async def read_all(self, 
                   session: AsyncSession,
                   statement: Select[tuple[Common]]) -> Sequence[Common]:
        entities: Result[tuple[Common]] = await session.execute(statement)
        return entities.scalars().unique().all()
    
    async def read_one(self, 
                   session: AsyncSession,
                   statement: Select[tuple[Common]]) -> Common | None:
        entities: Result[tuple[Common]] = await session.execute(statement)
        return entities.scalars().unique().one_or_none()
    
    async def update(self, id: UUID, session: AsyncSession, author_id: UUID, **new_data) -> Common:
        statement: Select[tuple[Common]] = select(self.Model).where(self.Model.id == id)
        result: Result[tuple[Common]] = await session.execute(statement)
        entity: Common = result.scalars().one()
        for attribute, value in new_data.items():
            if value:            
                setattr(entity, attribute, value)
        entity.modified_at = datetime.now()
        entity.modified_by = author_id
        session.add(instance=entity)
        return entity
    
    async def delete(self, session: AsyncSession, id: UUID) -> None:
        statement: Select[tuple[Common]] = select(self.Model).where(self.Model.id == id)
        result: Result[tuple[Common]] = await session.execute(statement=statement)
        entity: Common | None = result.scalar_one_or_none()
        if entity:
            await session.delete(instance=entity)
            await session.flush()
    