""" Compose 가 전달한 환경변수를 읽어서 코드에서 사용할 설정 객체로 만든다.
    예를 들어 포트 "3306"을 정수 3306 으로 변환하고,
    필수 설정이 빠지면 오류를 출력한다.
     
    1. pydantic_settings 에서 BaseSettings 를 import 한다.
    2. BaseSettings 을 상속하는 Setting 클래스를 정의한다.
    3. 클래스 안에 아래 항목을 타입과 함께 선언한다.
    4. 클래스 바깥에서 settings = Settings() 로 객체를 생성한다. """


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ 여기에 필드 선언 """

    # 필수 설정
    MYSQL_HOST: str
    # 값이 없으면 기본값을 사용
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str


settings = Settings()