""" 회원가입, 로그인, 회원탈퇴, 토큰 등을 관리하는 라우터 영역.
    서드파티 로그인 OAuth 연결 및 관리도 포함한다. """



# prefix 와 붙어서 경로는 POST v1/auth/signup 이 된다.
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.auth_schemas import UserCreate, UserResponse
from app.modules.auth.auth_service import AuthService


router = APIRouter(prefix="/auth")
auth_svc = AuthService

@router.post("/signup", response_model = UserResponse, status_code=201)
def signup(data:UserCreate, db: Session=Depends(get_db)):
    
    return auth_svc.create_me(db, data)