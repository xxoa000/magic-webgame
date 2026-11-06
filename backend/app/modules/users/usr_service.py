""" 회원가입 등 회원 관련 처리 로직. """

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users import usr_repository
from app.modules.users.usr_model import User
from app.modules.users.usr_schema import UserCreate


def create_user(db: Session, data: UserCreate) -> User:
    """ 아이디 중복을 확인하고 새 회원을 생성한다. """
    # 아이디로 DB 호출 결과.
    existing_user = usr_repository.get_by_username(db, data.username)

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="이미 사용 중인 아이디다.",
        )
    # data: 검증된 요청 데이터
    # user: DB 에 저장할 모델 객체
    user = User(
        username=data.username,
        password_hash=hash_password(data.password)
    )
    # 여기까지--회원 객체가 메모리에 생성된 상태.

    usr_repository.add_user(db, user)

    # 제약 추가: 동시에 같은 아이디로 가입할 때 발생하는 중복 오류 처리.
    try:
        db.commit()
        return user
    
    except IntegrityError as exc:
        db.rollback()
        # exc.orig.args에서 MySQL 오류 코드와 메시지를 꺼낸다.
        # 중복키 오류코드는 1062.
        error_code = exc.orig.args[0]
        error_message = exc.orig.args[1]

        # .endswith(): 메세지 끝에 적힌 키가 username 의 고유 인덱스인지 확인하는 메서드.
        if error_code == 1062 and error_message.endswith(
            ("for key 'username'", "for key 'users.username'")
        ):
            raise HTTPException(
                status_code=409,
                detail="이미 사용중인 아이디입니다."
            )
        # 인자 없는 raise: 방금 잡은 예외를 다시 올린다는 뜻.
        raise
