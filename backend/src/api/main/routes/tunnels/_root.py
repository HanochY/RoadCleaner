from fastapi import APIRouter
from api.main.routes.tunnels.cisco import router as cisco_router
from api.main.routes.tunnels.juniper import router as juniper_router

router = APIRouter(prefix="/tunnel", tags=["tunnel"])
router.include_router(cisco_router)
router.include_router(juniper_router)