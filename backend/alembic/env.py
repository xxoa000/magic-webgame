from logging.config import fileConfig

from app.core.base import Base
from app.core.database import database_url, engine
from app.modules.users.usr_model import User

from alembic import context

# Alembic 설정 객체.
# 사용 중인 .ini 파일의 설정값에 접근할 수 있다.
config = context.config

# 설정 파일에 정의된 로깅 설정을 적용한다.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 마이그레이션 자동 생성을 위해 모델의 메타데이터를 지정한다.
# 예시:
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# env.py에서 필요한 다른 설정값도 가져올 수 있다.
# 예시:
# my_important_option = config.get_main_option("my_important_option")


def run_migrations_offline() -> None:
    """오프라인 모드로 마이그레이션을 실행한다.

    엔진 대신 DB 접속 URL만으로 마이그레이션 환경을 설정한다.
    엔진을 전달하는 방식도 사용할 수 있다.

    엔진 생성을 생략하면 이 모드 자체에서는
    DBAPI 드라이버도 필요하지 않다.

    이 모드에서 context.execute()를 호출하면
    SQL을 DB에서 실행하는 대신 스크립트 출력으로 내보낸다.
    """
    url = database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()