""" 비밀번호 해시 및 JWT 인증 관련 보안(예정) 기능. """

from pwdlib import PasswordHash

# password_hasher: 비밀번호를 해시하고 검증할 객체
password_hasher = PasswordHash.recommended()

def hash_password(password:str) -> str:
    # 해시 결과 변환
    return password_hasher.hash(password)

def verify_password(password:str, hashed_password:str) -> bool:
    return password_hasher.verify(password, hashed_password)