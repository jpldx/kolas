from fastapi import APIRouter
from . import host_router

router = APIRouter()

# 路由挂载
router.include_router(host_router.router, prefix="/host", tags=["主机管理"])
