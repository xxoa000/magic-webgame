""" MySQL 연결을 관리하는 엔진. """

from sqlalchemy import URL, create_engine
from app.core.config import settings
from collections.abc import Generator
from sqlalchemy.orm import Session, sessionmaker


# URL.create() 로 접속 정보 구성
# utf8mb4: 한글과 이모지 등을 저장할 수 있는 문자 인코딩 설정.
database_url = URL.create(
    drivername = "mysql+pymysql",
    username = settings.MYSQL_USER,
    password = settings.MYSQL_PASSWORD,
    host = settings.MYSQL_HOST,
    port = settings.MYSQL_PORT,
    database = settings.MYSQL_DATABASE,
    query = {"charset":"utf8mb4"},
)

# 엔진 생성
# engine: DB 접속과 연결 풀을 관리 하는 객체
# pool_pre_ping=True: 풀에서 연결을 꺼낼때 아직 유효한 연결인지 확인한다.
# pool: 필요할 때 꺼내 쓰려고 자원을 모아두는 공간.
#       DB에 접속할 때마다 연결을 새로 만들면 통신 연결과 인증을 반복해야 한다.
#       그래서 만들어둔 연결을 재사용한다.
engine = create_engine(database_url, pool_pre_ping=True)

# 아직 실제 쿼리 실행 x 인 상태.


""" DB 세션을 만들어주는 도구. """
SessionLocal = sessionmaker(
    bind=engine,        # 기존 MySQL 엔진 사용
    autoflush=False,    # 조회 전에 대기 중인 변경 사항을 자동 전송하지 않음
)

def get_db() -> Generator[Session, None, None]:
    """ 요청 처리에 사용할 DB 세션을 제공하고 종료한다. """

    with SessionLocal() as session:
        yield session
