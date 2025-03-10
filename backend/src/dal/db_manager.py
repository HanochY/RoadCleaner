
from config.provider import ConfigProvider
from dal.models._base import Base
from utils.enums.vendor import Vendor
from dal.models.device_type import DeviceType
from dal.models.device import Device
from dal.models.interface import Interface
from dal.models.site import Site
from dal.models.tunnel._base import Tunnel
from dal.models.tunnel.cisco import CiscoTunnel
from dal.models.tunnel.juniper import JuniperTunnel
from dal.models.task import Task
from dal.models.user import User

import contextlib
from typing import Any, AsyncIterator
#from _collections_abc import AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

forum_db_settings = ConfigProvider.forum_db_settings(production=False)
DATABASE_URL = forum_db_settings.ASYNC_URI


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            
    async def init_db(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as conn: 
            await conn.run_sync(Base.metadata.create_all)

            async with session_manager.session() as session:
                type = DeviceType(name=Vendor.CISCO)
            # Example data insertion
                session.add_all([
                    DeviceType(name=Vendor.CISCO),
                    DeviceType(name=Vendor.JUNIPER)
                ])
                await session.commit()


session_manager = DatabaseSessionManager(DATABASE_URL)


async def generate_db_session():
    async with session_manager.session() as session:
        yield session