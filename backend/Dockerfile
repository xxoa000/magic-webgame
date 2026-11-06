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