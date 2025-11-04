from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing import Any


from db.database import get_session
from core.settings import Settings
from models.user import User


SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


class TokenType:
    ACCESS = 'access'
    REFRESH = 'refresh'


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def verify_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type: str = payload.get('type')
        if token_type not in [TokenType.ACCESS, TokenType.REFRESH]:
            raise JWTError('Tipo de Token inválida')
        return payload
    except (JWTError, ValidationError):
        raise HTTPException(status_code=401, detail='Token inválida')


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or
                                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire, 'type': TokenType.ACCESS})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp': expire, 'type': TokenType.REFRESH})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token inválido ou expirado',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def require_privilegio(required_privilegios: list[str]):
    def wrapper(
            current_user: dict = Depends(get_current_user)
        ):
        if current_user.privilegio.nome not in required_privilegios:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Você não tem permissão para acessar este recurso'
            )
        return current_user

    return wrapper

    
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        token = credentials.credentials
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=401,
                detail='Token inválido ou expirado'
            )
        return payload