""" 회원 요청 및 응답 데이터 스키마. """

from pydantic import BaseModel, ConfigDict, Field

# BaseModel: 요청, 응답 데이터 구조오 검증 규칙 정의
class UserCreate(BaseModel):
    """ 회원가입 요청 데이터와 입력값 검증 규칙. """
    username: str = Field(
        min_lengh=4,
        max_lengh=50,
        pattern=r"^[a-z0-9_]+$",
    )
    password: str = Field(
        min_lengh=8,
        max_lengh=128,
        pattern=r"^[a-z0-9_]+$",
    )

class UserResponse(BaseModel):
    id: int
    username: str
    # ConfigDict(): Pydantic 모델의 동작 방식을 정하는 설정용 딕셔너리.
    # from_attributes=True: 
    #   Pydantic 이 SQLAlchemy 의 User 객체에서 user.id, user.username 같은 속성에서 값을 읽게 하는 설정.
    model_config = ConfigDict(from_attributes=True)