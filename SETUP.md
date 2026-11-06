새 프로젝트 만들기.

# 전체 프로젝트 폴더 생성
`cd ~/원하는 폴더 위치로 이동`  
`mkdir 폴더명` : 폴더 생성  
`cd 폴더명`  

## Git 초기 설정
`git init -b main` : 로컬 Git 저장소 만들고 main 브랜치 만들기.  
&nbsp;&nbsp;&nbsp;&nbsp; `-b`: -initial-branch 의 축약어. 초기 브랜치 설정.  
`git status` : Git 생성 확인
`code .` : vscode 에서 폴더 열기  


## 프론트엔드 프로젝트 생성
`node -v` , `npm -v` : 현재 설치 버전 확인  
`npx create-next-app@latest frontend` : 프론트 프로젝트 생성  
추천 설정대로 설치하는 방법 과 직접 설정을 커스텀해서 설치하는 방법이 있음.  


### Docker compose 설정하기
Docker compose 로 lib 를 관리하되, vscode 도 해당 컨테이너와 연결할 수 있도록 확장프로그램 Dev Containers 설치.

#### frontend/Dockerfile 파일 작성
```
# Node.js 24 가 설치된 Linux 이미지를 기반으로 사용.
FROM node:24-bookworm-slim

# 컨테이너 내부 작업 폴더를 /app 으로 지정
WORKDIR /app

# 패키지 목록과 버전 기록을 작업 폴더에 복사
COPY package.json package-lock.json ./

# 기록된 버전대로 패키지 설치
RUN npm ci

# 프론트 소스를 작업 폴더에 복사
COPY . .

# 앱이 사용하는 포트를 문서화
# EXPOSE 만으로 맥에서 접속할 수 있는 건 아니고, 포트 연결은 Compose 가 설정한다.
EXPOSE 3000

# 컨테이너 시작 시 개발 서버 실행
# RUN 은 이미지를 만들 때, CMD 는 컨테이너를 실행할 때 사용한다.
# -- : 뒤에 있는 옵션을 npm 이 아니라 실제 개발 서버 명령에 전달한다는 뜻.
# 0.0.0.0 : 컨테이너 밖에서 들어오는 연결도 받을 수 있도록 지정한 주소.
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
```

#### frontend/.dockerignore 파일 작성
```
# 이 파일에는 이미지를 만들 때 복사 대상에서 제외할 항목을 적는다.
node_modules
.next
.git
.env*
npm-debug.log*
```

### 최상위 폴더 위치에서 compose.yaml 파일 작성
```
services:
    frontend:
        build:
            # build.context: frontend/Dockerfile 로 이미지 생성
            context: ./frontend
        ports:
            # 맥의 5175 port 를 컨테이너의 3000 port 에 연결
            - "127.0.0.1:5175:3000"
        volumes:
            # 왼쪽:오른쪽 -> 왼쪽의 저장공간을 오른쪽에 컨테이너 경로에 연결해라 라는 의미.
            # 로컬의 frontend 파일을 컨테이너 기본 폴더로 지정한 /app 과 연결.(Dockerfile 참고.)
            - ./frontend:/app
            # /app/node_modules: npm의 패키지 설치 방식
            # 운영체제가 달라져도 문제 없도록 설치한 외부 패키지는 컨테이너에도 따로 보관.
            - frontend_node_modules:/app/node_modules
            # /app/.next: Next.js 프로젝트 구조, 빌드 설명 
            # 작성한 소스를 브라우저와 서버에서 실행할 형태로 빌드한 결과물과, 다음 변환을 빠르게 처리하기 위해 쌓이는 캐시 등이 .next 폴더에 들어간다.
            - frontend_next:/app/.next

# Docker가 관리할 볼륨(저장공간) 이름을 정한다.
volumes:
    # 컨테이너용 패키지를 별도 보관 (Next.js, React, TypeScript 등)
    frontend_node_modules:
    # Next.js가 생성하는 빌드,캐시 파일을 별도 보관
    frontend_next:
```  

직접 터미널에서 컨테이너 내부 쉘을 확인하는 코드  
`docker compose exec frontend sh` : 최상위 폴더 위치에서 명령어 입력, frontend 쉘을 연다.  
`pwd` : 현재 위치 확인  
`ls -la` : 현재 폴더의 파일 목록 확인. -a 가 있어야 . 으로 시작하는 폴더도 보임  
`ls /` : 컨테이너의 최상의 폴더들 확인.  
`exit` : 쉘 나오기  


#### vscode - 컨테이너 연결하기
1. Cmd + Shift + P로 명령 팔레트를 열기.
2. Dev Containers: Attach to Running Container...를 검색해서 선택.
3. 목록에서 magic-webgame-frontend-1처럼 frontend가 포함된 컨테이너를 선택.
4. 새 VS Code 창이 열리면 파일 → 폴더 열기에서 /app을 연다.
컨테이너 내부의 가상공간이 열린다. 내부에서 작업하더라도 내 컴퓨터와는 소스를 공유한다.


## 백엔드 프로젝트 생성
```
root-project/
├── compose.yaml
├── frontend/
└── backend/
    ├── requirements.txt
    └── app/
        ├── __init__.py
        └── main.py
```
직접 폴더를 생성하는 방법과, 터미널 명령어를 이용해 만드는 방법이 있다.
```
mkdir -p backend/app
touch backend/requirements.txt backend/app/__init__.py backend/app/main.py
```

#### requirements.txt
```
# 설치할 파이썬 패키지(의존성 목록)를 적어두는 파일.
# 'python -m pip install -r requirement.txt' 명령어를 실행하면 목록에 있는 패키지를 설치한다.
# 추후 Dockerfile 파일에 해당 명령어를 넣어서 컨테이너 안에 설치할 예정임. """ 

# FastAPI: API 주소와 요청 처리 로직을 작성하는 프레임워크.
fastapi

# Uvicorn: FastAPI 앱을 실행하고 HTTP 요청을 받는 서버 프로그램.
# [standard]: 권장 추가 의존성도 함께 설치한다는 뜻.
uvicorn[standard]
```


#### main.py 파일 기본코드 작성
```
""" FastAPI 앱의 시작 파일. 

    1. fastapi에서 FastAPI 클래스를 import 한다.
    2. FastAPI()로 객체를 생성하고 app 변수에 넣는다.
    3. /health 요청을 처리할 함수를 정의한다.
    4. 함수 위에 @app.get("/health")를 붙여, GET /health 요청과 해당 함수를 연결한다.
    5. 함수는 파이썬 딕셔너리 {"status": "ok"}를 JSON 응답으로 반환하게 한다. """

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    """ 서버가 요청을 받고 응답할 수 있는지 확인하는 기능. 
        현재는 DB 연결, 유효성 검사 없이 오로지 응답 여부만 확인한다. """

    return {"status":"ok"}
```


#### backend/Dockfile 파일 작성
```
# Python 3.14 가 설치된 이미지를 사용
FROM python:3.14-slim

# 컨테이너 작업 위치 지정
WORKDIR /app

# 패키지 목록을 /app 에 복사
COPY requirements.txt ./

# 미리 작성해둔 requirements.txt 파일을 사용하여 컨테이너 이미지 안에 패키지 설치
RUN python -m pip install --no-cache-dir -r requirements.txt

# 맥의 backend/app 을 컨테이너의 /app/app 에 복사
COPY ./app ./app

# 서버가 사용할 포트 표시
EXPOSE 8000

# 컨테이너 시작 시 Uvicorn 으로 앱 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 최상위 폴더 위치에서 compose.yaml 파일에 backend 코드 추가
```
services:
    frontend:
        ...

    backend:
        build:
            # backend Dockerfile 로 이미지 생성
            context: ./backend
        ports:
            # 맥의 8002 를 컨테이너의 8000 에 연결
            - "127.0.0.1:8002:8000"
        volumes:
            # backend 소스를 연결해서 수정 사항 반영
            # 파이썬 패키지는 /app 바깥의 파이썬 설치 경로에 설치되므로,
            # 프론트의 node_modules 처럼 별도 볼륨을 추가할 필요할 필요는 없다.
            - ./backend:/app
```

`docker compose up --build -d backend` : 실행 후 Backend localhost의 docs 를 열어서 health ok 확인

#### vscode - 컨테이너 연결
Frontend 와 같은 방식으로 연결 후 확장프로그램 Python, Pylance 설치.

## Git 제외 파일 설정

최상위 폴더에 `.gitignore`를 작성한다. 이미 있다면 필요한 항목만 추가한다.

```gitignore
# Python 가상환경과 임시 파일
.venv/
__pycache__/
*.pyc

# 실제 환경변수 파일 제외
.env
.env.*

# 환경변수 예시 파일은 Git에 포함
!.env.example
```

`frontend/.gitignore`는 프론트 폴더에 적용된다. 최상위 `.gitignore`는 백엔드를 포함한 프로젝트 전체에 적용된다.

| 파일 | 역할 |
|---|---|
| `.gitignore` | Git에 기록하지 않을 파일 지정 |
| `.dockerignore` | Docker 빌드에 전달하지 않을 파일 지정 |

### backend/.dockerignore 작성

```text
.venv
__pycache__
*.pyc
.git
.env*
```

## 환경변수 파일 생성

맥의 최상위 프로젝트 폴더에서 작업한다.

컨테이너 창의 `/app`은 각각 프론트 또는 백엔드 폴더이므로 최상위 프로젝트 폴더와 구분한다.

### .env.example 작성

`compose.yaml`과 같은 위치에 생성한다.

```dotenv
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=magic_webgame
MYSQL_USER=magic_user
MYSQL_PASSWORD=
MYSQL_HOST_PORT=3309

REDIS_PASSWORD=
```

| 변수 | 역할 |
|---|---|
| `MYSQL_ROOT_PASSWORD` | MySQL 관리자 계정 비밀번호 |
| `MYSQL_DATABASE` | 최초 생성할 DB 이름 |
| `MYSQL_USER` | 백엔드가 사용할 일반 계정 |
| `MYSQL_PASSWORD` | 일반 계정 비밀번호 |
| `MYSQL_HOST_PORT` | 맥에서 MySQL에 접속할 포트 |
| `REDIS_PASSWORD` | Redis 인증 비밀번호 |

### .env 생성

최상위 폴더의 맥 터미널에서 실행한다.

```bash
cp -n .env.example .env
```

`-n`은 기존 `.env`가 있을 때 덮어쓰지 않는 옵션이다.

무작위 비밀번호 생성:

```bash
openssl rand -hex 24
```

48자리 무작위 문자열을 생성한다. 비밀번호마다 새 값을 생성해 `.env`에 입력한다.

| 파일 | 내용 | Git 기록 |
|---|---|---|
| `.env.example` | 필요한 변수와 예시 값 | 포함 |
| `.env` | 실제 설정과 비밀번호 | 제외 |

## Compose에 MySQL과 Redis 추가

기존 `services` 아래에 `frontend`, `backend`와 같은 계층으로 추가한다.

```yaml
    mysql:
        image: mysql:8.4
        environment:
            MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
            MYSQL_DATABASE: ${MYSQL_DATABASE}
            MYSQL_USER: ${MYSQL_USER}
            MYSQL_PASSWORD: ${MYSQL_PASSWORD}
        ports:
            - "127.0.0.1:${MYSQL_HOST_PORT:-3309}:3306"
        volumes:
            - mysql_data:/var/lib/mysql

    redis:
        image: redis:8-alpine
        command:
            - redis-server
            - --appendonly
            - "yes"
            - --requirepass
            - "${REDIS_PASSWORD:?REDIS_PASSWORD is required}"
        volumes:
            - redis_data:/data
```

| 설정 | 의미 |
|---|---|
| `image` | 준비된 이미지 사용 |
| `${MYSQL_DATABASE}` | Compose가 `.env`에서 값을 가져옴 |
| `${MYSQL_HOST_PORT:-3309}` | 값이 없거나 비어 있으면 `3309` 사용 |
| `${REDIS_PASSWORD:?…}` | 값이 없거나 비어 있으면 오류 발생 |
| `--appendonly yes` | Redis 변경 내용을 디스크에 기록 |
| `--requirepass` | Redis 접속 시 비밀번호 요구 |

`${변수:?오류문구}`에서 `:`와 `?` 사이에는 공백을 넣지 않는다.

Redis는 맥에 포트를 공개하지 않고, 같은 Compose 네트워크의 백엔드에서 접근한다.

### 기존 볼륨 선언에 추가

최하단의 기존 `volumes`에 추가한다. `volumes:`를 중복 선언하지 않는다.

```yaml
volumes:
    frontend_node_modules:
    frontend_next:
    mysql_data:
    redis_data:
```

| 볼륨 | 연결 위치 | 저장 내용 |
|---|---|---|
| `mysql_data` | `/var/lib/mysql` | MySQL 데이터 |
| `redis_data` | `/data` | Redis 영속화 데이터 |

### 실행 및 상태 확인

맥의 최상위 프로젝트 터미널에서 실행한다.

```bash
docker compose up -d mysql redis
```

컨테이너 상태 확인:

```bash
docker compose ps -a
```

로그 확인:

```bash
docker compose logs --tail=30 mysql redis
```

확인할 로그:

- MySQL: `ready for connections`
- Redis: `Ready to accept connections`

MySQL의 계정·비밀번호·DB 환경변수는 최초 초기화에 사용된다. 초기화 후 `.env`의 비밀번호만 변경해도 기존 DB 계정의 비밀번호가 자동 변경되지는 않는다.

`docker compose down`은 일반적으로 이름 있는 볼륨을 유지한다.

**`docker compose down -v`는 볼륨과 저장된 데이터까지 삭제하므로 주의한다.**

## 백엔드 연결용 패키지 추가

`backend/requirements.txt`에 기존 패키지를 유지하고 추가한다.

```text
# API 프레임워크와 실행 서버
fastapi
uvicorn[standard]

# MySQL ORM 및 드라이버
sqlalchemy
pymysql[rsa]

# Redis 클라이언트
redis

# 환경변수 로딩과 검증
pydantic-settings
```

| 패키지 | 역할 |
|---|---|
| `sqlalchemy` | SQL 실행, ORM 및 연결 풀 관리 |
| `pymysql[rsa]` | MySQL 접속과 인증용 추가 의존성 |
| `redis` | Redis 접속과 명령 실행 |
| `pydantic-settings` | 환경변수 로딩과 타입 검증 |

현재는 버전을 지정하지 않았다. 같은 환경을 재현하려면 이후 의존성 버전을 고정한다.

`requirements.txt`는 파이썬 코드가 아니므로 설명은 `"""`가 아닌 `#` 주석으로 작성한다.

## 백엔드에 환경변수 전달

기존 Compose의 `backend` 설정에 `environment`를 추가한다.

```yaml
    backend:
        build:
            context: ./backend
        ports:
            - "127.0.0.1:8002:8000"
        volumes:
            - ./backend:/app
        environment:
            MYSQL_HOST: mysql
            MYSQL_PORT: "3306"
            MYSQL_DATABASE: ${MYSQL_DATABASE}
            MYSQL_USER: ${MYSQL_USER}
            MYSQL_PASSWORD: "${MYSQL_PASSWORD:?MYSQL_PASSWORD is required}"
            REDIS_HOST: redis
            REDIS_PORT: "6379"
            REDIS_PASSWORD: "${REDIS_PASSWORD:?REDIS_PASSWORD is required}"
```

최상위 `.env`는 Compose가 읽는다.

백엔드는 `.env` 파일을 직접 읽는 대신, `backend.environment`로 전달받은 환경변수를 사용한다.

백엔드는 일반 계정으로 MySQL에 접속하므로 `MYSQL_ROOT_PASSWORD`는 전달하지 않는다.

### 맥 접속과 컨테이너 간 접속 구분

| 접속하는 곳 | 대상 | 호스트 | 포트 |
|---|---|---|---|
| 맥의 DBeaver 등 | MySQL | `127.0.0.1` | `MYSQL_HOST_PORT` 값 |
| 백엔드 컨테이너 | MySQL | `mysql` | `3306` |
| 백엔드 컨테이너 | Redis | `redis` | `6379` |

컨테이너끼리는 서비스 이름과 컨테이너 내부 포트를 사용한다.

### 패키지 설치와 설정 반영

맥의 최상위 프로젝트 터미널에서 실행한다.

```bash
docker compose up --build -d backend
```

패키지 변경 없이 환경변수만 변경한 경우:

```bash
docker compose up -d --force-recreate backend
```

환경변수는 컨테이너 생성 시 전달되므로 Uvicorn의 자동 리로드만으로는 변경되지 않는다.

백엔드 컨테이너 재생성 후 VS Code 연결이 끊기면 다시 연결한다.

## 환경변수를 읽는 config.py 작성

백엔드 컨테이너의 VS Code 창에서 다음 파일을 만든다.

```text
app/core/
├── __init__.py
└── config.py
```

`__init__.py`는 빈 파일로 둔다.

### app/core/config.py

```python
"""백엔드 환경변수 설정."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str


settings = Settings()
```

`BaseSettings`는 환경변수를 읽고 선언한 타입에 맞게 변환·검증한다.

- 기본값 없는 필드: 값이 전달되지 않으면 오류 발생
- 기본값 있는 필드: 값이 없으면 기본값 사용
- `settings = Settings()`: 클래스 정의가 끝난 뒤 객체 생성

| 선언 예시 | 의미 |
|---|---|
| `MYSQL_HOST: str` | 필수이며 문자열이어야 함 |
| `MYSQL_HOST: str \| None` | 필수지만 `None`도 허용 |
| `MYSQL_HOST: str \| None = None` | 생략 가능하며 기본값은 `None` |

이번 설정에서는 Compose가 환경변수를 전달하므로 `.env` 파일 경로를 별도로 지정하지 않는다.

### 설정 로딩 확인

백엔드 컨테이너 터미널에서 실행한다.

```bash
python -c "from app.core.config import settings; print(settings.MYSQL_HOST, settings.MYSQL_PORT, settings.REDIS_HOST, settings.REDIS_PORT)"
```

정상 출력:

```text
mysql 3306 redis 6379
```

비밀번호 등 민감한 설정은 출력하지 않는다.

`Field required` 오류가 나오면 Compose의 `backend.environment`에 해당 변수가 있는지 확인한다. 수정 후 컨테이너를 재생성한다.

## MySQL 연결 엔진 생성

### app/core/database.py

```python
"""MySQL 연결을 관리하는 엔진."""

from sqlalchemy import URL, create_engine

from app.core.config import settings


database_url = URL.create(
    drivername="mysql+pymysql",
    username=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    host=settings.MYSQL_HOST,
    port=settings.MYSQL_PORT,
    database=settings.MYSQL_DATABASE,
    query={"charset": "utf8mb4"},
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)
```

| 항목 | 역할 |
|---|---|
| `URL.create()` | 접속 정보로 URL 객체 구성 |
| `mysql+pymysql` | MySQL과 PyMySQL 드라이버 사용 |
| `utf8mb4` | 한글과 이모지 등을 위한 문자 인코딩 |
| `engine` | DB 연결과 연결 풀 관리 |
| `pool_pre_ping=True` | 풀에서 연결을 가져올 때 유효성 확인 |

연결 풀은 DB 연결을 빌려 쓰고 반환하여 재사용하는 구조다.

1. 요청이 들어온다.
2. 풀에서 연결을 가져온다.
3. SQL을 실행한다.
4. 작업이 끝나면 연결을 풀에 반환한다.
5. 다음 요청이 연결을 재사용한다.

처음이거나 사용 가능한 연결이 없으면 풀 설정 범위 안에서 새 연결을 만들 수도 있다.

엔진 생성만으로 실제 접속이 확인되는 것은 아니다.

### 실제 MySQL 연결 확인

백엔드 컨테이너 터미널에서 실행한다. 확인 코드는 `database.py`에 추가하지 않는다.

```bash
python - <<'PY'
from sqlalchemy import text
from app.core.database import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar_one())
PY
```

| 코드 | 역할 |
|---|---|
| `engine.connect()` | 실제 DB 연결 가져오기 |
| `text("SELECT 1")` | 실행할 SQL 구성 |
| `execute(...)` | SQL 실행 |
| `scalar_one()` | 결과에서 단일 값 가져오기 |
| `with` | 블록 종료 시 연결을 풀에 반환 |

`1`이 출력되면 접속·인증·SQL 실행까지 성공한 것이다.

## Redis 클라이언트 생성

### app/core/redis_client.py

```python
"""Redis 접속용 클라이언트."""

from redis import Redis

from app.core.config import settings


redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
)
```

| 인자 | 역할 |
|---|---|
| `host` | Redis 호스트 |
| `port` | Redis 포트 |
| `password` | 인증 비밀번호 |
| `decode_responses=True` | 텍스트 응답을 문자열로 변환 |
| `socket_connect_timeout=5` | 연결 대기 제한 5초 |
| `socket_timeout=5` | 응답 대기 제한 5초 |

객체 생성만으로 실제 접속이 확인되는 것은 아니다.

### 실제 Redis 연결 확인

백엔드 컨테이너 터미널에서 실행한다.

```bash
python -c "from app.core.redis_client import redis_client; print(redis_client.ping()); redis_client.close()"
```

`True`가 출력되면 접속·인증·응답 확인까지 성공한 것이다.

## 현재 완료한 단계

- Next.js 프로젝트 생성
- 프론트·백엔드 Dockerfile과 Compose 설정
- Dev Containers를 통한 VS Code 연결
- FastAPI `/health` 응답 확인
- MySQL·Redis 실행
- 백엔드 환경변수 로딩 확인
- 백엔드에서 MySQL·Redis 실제 접속 확인

## 다음 작업

FastAPI CORS 설정 후 Next.js 화면에서 `/health`를 호출해 응답을 표시한다.
