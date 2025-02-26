from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import logging.config

from config.provider import ConfigProvider
from dal.db_manager import session_manager
from api.main.routes.authentication_ldap import router as authentication_ldap_router
from api.main.routes.authentication import router as authentication_router
from api.main.routes.device_type import router as device_type_router
from api.main.routes.device import router as device_router
from api.main.routes.interface import router as interface_router
from api.main.routes.site import router as site_router
from api.main.routes.tunnels.tunnels import router as tunnel_router
from api.main.routes.user import router as user_router

from api.main.middleware.logging import LoggingMiddleware
from contextlib import asynccontextmanager
    
app_settings = ConfigProvider.main_app_settings()
app_metadata = ConfigProvider.metadata()
logging_settings = ConfigProvider.logging_settings()
@asynccontextmanager
async def lifespan(app: FastAPI):
    await session_manager.init_db()
    logging.config.dictConfig(logging_settings)
    yield
    
app = FastAPI(root_path="/api",
              title=app_metadata.NAME,
              description=app_metadata.DESCRIPTION,
              version=app_metadata.VERSION,
              responses={404: {"description": "Not found"}},
              lifespan=lifespan
              )

if app_settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            app_settings.ALLOWED_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
app.add_middleware(LoggingMiddleware)
#app.include_router(ldap_authentication_router)
app.include_router(authentication_router)
app.include_router(device_type_router)
app.include_router(device_router)
app.include_router(interface_router)
app.include_router(site_router)
app.include_router(tunnel_router)
app.include_router(user_router)
