""" FastAPI 앱의 시작 파일. 

    1. fastapi에서 FastAPI 클래스를 import 한다.
    2. FastAPI()로 객체를 생성하고 app 변수에 넣는다.
    3. /health 요청을 처리할 함수를 정의한다.
    4. 함수 위에 @app.get("/health")를 붙여, GET /health 요청과 해당 함수를 연결한다.
    5. 함수는 파이썬 딕셔너리 {"status": "ok"}를 JSON 응답으로 반환하게 한다. """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import v1_router


app = FastAPI()
# router 경로 앞에 /v1 을 붙이는 코드
app.include_router(v1_router)


""" Next.js 화면에서 FastAPI 응답을 받아 표시하기. """
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175"],
    allow_methods=["GET"]
)

@app.get("/health")
def health():
    """ 서버가 요청을 받고 응답할 수 있는지 확인하는 기능. """

    return {"status":"ok"}
