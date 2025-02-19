from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import ColumnExpressionArgument, select
from dal.models._base import Common
from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

class SQLAlchemyRepository():
    Model: type[Common]
    
    def __init__(self, Model: type[Common]):
        self.Model = Model
        
    async def create(self, session: AsyncSession, author_id: UUID, **data) -> Common:
        print(self.Model)
        entity = self.Model(**data)
        entity.created_at = datetime.now()
        entity.created_by = author_id
        entity.modified_at = datetime.now()
        entity.modified_by = author_id
        session.add(entity)
        print(str(entity))
        return entity
        
    async def read(self, 
                   session: AsyncSession,
                   filter: ColumnExpressionArgument | None = None, 
                   offset: int | None = None, 
                   limit: int | None = None) -> Sequence[Common]:
        statement = select(self.Model)
        if filter:
            statement = statement.where(filter)
        if offset:
            statement = statement.offset(offset)
        if limit: 
            statement = statement.limit(limit)
        print(statement)
        entities = await session.execute(statement)
        return entities.scalars().all()
    
    async def update(self, session: AsyncSession, author_id: UUID, **new_data) -> Common:
        statement = select(self.Model).where(self.Model.id == id)
        result = await session.execute(statement)
        entity: Common = result.scalars().one()
        for attribute, value in new_data.items():
            setattr(entity, attribute, value)
        entity.modified_at = datetime.now()
        entity.modified_by = author_id
        session.add(entity)
        return entity

    async def delete(self, session: AsyncSession, author_id: UUID, id: UUID) -> Common:
        statement = select(self.Model).where(self.Model.id == id)
        result = await session.execute(statement)
        entity = result.scalars().one()
        if not entity.is_deleted:
            entity.deleted_at = datetime.now()
            entity.deleted_by = author_id
            entity.is_deleted = True
            session.add(entity)
        return entity
    
    async def undelete(self, session: AsyncSession, id: UUID) -> Common:
        statement = select(self.Model).where(self.Model.id == id)
        result = await session.execute(statement)
        entity = result.scalars().one()
        if entity.is_deleted:
            entity.is_deleted = False
            session.add(entity)
        return entity
    
    async def hard_delete(self, session: AsyncSession, id: UUID) -> None:
        statement = select(self.Model).where(self.Model.id == id)
        result = await session.execute(statement)
        entity = result.scalars().one()
        if entity:
            session.delete(result)
    