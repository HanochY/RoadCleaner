from dal.db_manager import DatabaseSessionManager, DATABASE_URL, create_defaults
import asyncio

manager = DatabaseSessionManager(DATABASE_URL)
asyncio.run(manager.init_db())
asyncio.run(create_defaults())