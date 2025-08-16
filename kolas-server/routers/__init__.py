from fastapi import APIRouter
from . import host_router, project_router, file_router

router = APIRouter()

# 路由挂载
router.include_router(project_router.router, prefix="/project", tags=["项目管理"])
router.include_router(file_router.router, prefix="/file", tags=["文件上传"])
router.include_router(host_router.router, prefix="/host", tags=["主机管理"])
