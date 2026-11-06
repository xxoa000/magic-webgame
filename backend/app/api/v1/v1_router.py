""" v1 로 버전 관리. 이후 업데이트시 v2, v3... 등등 """

from fastapi import APIRouter
from app.modules.users import usr_router as users_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(users_router)