## 컨테이너가 꺼져 있을때 다시 연결시키는 터미널 명령어
```bash
docker compose up -d --build frontend backend mysql redis
docker compose ps -a
```
첫 번째 명령어는 compose.yaml에 정의된 서비스를 시작합니다. 
컨테이너가 없으면 만들고, -d 옵션으로 백그라운드에서 실행해 터미널을 바로 돌려줍니다.

두 번째 명령어는 컨테이너의 상태를 보여줍니다. -a는 종료된 컨테이너도 포함합니다. 
Up 이면 실행 중이고, Exited 이면 종료된 상태입니다.

--build는 프런트엔드와 백엔드 이미지를 빌드합니다. 
ps -a에는 시작 직후 종료된 컨테이너도 표시됩니다.



## localhost 실행
``` bash
docker compose up -d backend
docker compose logs -f backend
```



## 정상 작동하지 않을 경우 확인
```bash
docker compose logs --tail=50 frontend backend
```
목록에는 보이는데 API가 응답하지 않거나 서비스가 Exited로 표시되면 -> 로그 확인.