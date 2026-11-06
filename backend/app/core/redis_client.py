""" Redis 연결 확인.

    1. redis 에서 Redis 클래스를 가져온다.
    2. app.core.config 에서 settings 를 가져온다.
    3. Redis(...) 객체를 만들어 redis_client 변수에 넣는다. 
    
    python -c "from app.core.redis_client import redis_client;
        print(redis_client.ping());
        redis_client.close()"
    터미널 명령어로 연결 확인 """

from redis import Redis
from app.core.config import settings


redis_client = Redis(
    host = settings.REDIS_HOST,         # Redis 호스트
    port = settings.REDIS_PORT,         # Redis 포트
    password = settings.REDIS_PASSWORD, # 인증 비밀번호
    decode_responses = True,            # 조회 결과를 문자열로 받기
    socket_connect_timeout = 5,         # 연결 대기 제한 5초
    socket_timeout = 5,                 # 응답 대기 제한 5초
)
