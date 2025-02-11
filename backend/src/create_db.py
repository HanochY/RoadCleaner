from dal.db_manager import DatabaseSessionManager, DATABASE_URL
import asyncio
manager = DatabaseSessionManager(DATABASE_URL)
asyncio.run(manager.init_db())
