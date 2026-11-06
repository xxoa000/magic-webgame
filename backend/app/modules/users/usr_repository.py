""" 회원 데이터 조회 및 저장. """

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.usr_model import User


def get_by_username(db: Session, username: str) -> User | None:
    """ 로그인 아이디로 회원을 조회한다. """
    statement = (
        select(User)
        .where(User.username == username)
    )
    return db.scalar(statement)


def add_user(db: Session, user: User) -> User:
    """ 새 회원을 세션에 추가한다. """
    db.add(user)
    return user