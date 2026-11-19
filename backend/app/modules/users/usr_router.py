
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.users.usr_schemas import UserCreate, UserResponse
from app.modules.users.usr_service import create_user

# APIRouter: FastAPI 에서 가져오는 클래스
router = APIRouter(prefix="/users")
    