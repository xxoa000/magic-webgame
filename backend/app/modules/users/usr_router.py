
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.users.usr_schema import UserCreate, UserResponse
from app.modules.users.usr_service import create_user

# APIRouter: FastAPI 에서 가져오는 클래스
router = APIRouter(prefix="/users")

# prefix 와 붙어서 경로는 POST v1/users/signup 이 된다.
@router.post("/signup", response_model = UserResponse, status_code=201)
def signup(data:UserCreate, db: Session=Depends(get_db)):
    

    return create_user(db, data)
    