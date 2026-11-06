""" User, Character 등의 DB 모델들이 공통으로 상속할 기준 클래스.
    모델의 테이블 정보가 Base 의 metadata 에 모이고, 추후 Alembic 이 그 정보를 참고한다. """

from datetime import datetime, timezone

# SQLAlchemy 가 제공하는 모델의 기준 클래스
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

# DeclarativeBase 를 상속해 우리 프로젝트의 공통 Base 정의
class Base(DeclarativeBase):
    """ 모든 table 에 created_at, updated_at 컬럼 자동 추가. """
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default = utc_now,
        nullable = False,
        comment="생성 시각, UTC.",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default = utc_now,  # 새 행을 저장할 때 현재 UTC 시각 기록
        onupdate=utc_now,   # UPDATE를 실행할 때 현재 UTC 시각 기록
        nullable = False,   # NULL 저장 금지
        comment="수정 시각, UTC.",
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="삭제 시각, UTC.",
    )
