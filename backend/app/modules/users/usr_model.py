""" 회원 DB 설정. """

from datetime import datetime
from sqlalchemy import BigInteger, CheckConstraint, DateTime, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("status IN (0, 1, 3, 9)", name="ck_users_status"),
        CheckConstraint("auth IN (0, 1, 9)", name="ck_users_auth"),
        {"comment": "회원 계정"},
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key = True,
        autoincrement = True,
        comment="회원 고유 번호",
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="로그인 아이디",
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="비밀번호 해시",
    )

    status: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=1,
        server_default="1",
        comment="계정 상태: 0=휴면, 1=활성, 3=제재, 9=탈퇴",
    )
    auth: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        default=0,
        server_default="0",
        comment="권한: 0=일반 회원, 1=스태프, 9=관리자"
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="마지막 로그인 성공 시각, UTC.",
    )