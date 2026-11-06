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