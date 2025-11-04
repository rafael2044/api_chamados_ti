from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token
)
from db.database import get_session
from schemas.token import Token
from schemas.tokenRefreshRequest import TokenRefreshRequest
from schemas.userLogin import UserLogin
from schemas.userRegister import UserRegister
from schemas.userResponse import UserResponse
from crud.user import crud_user

router = APIRouter(tags=['Auth'])


@router.post('/register', response_model=UserResponse)
def register_user(user: UserRegister, session: Session = Depends(get_session)):
    
    new_user = crud_user.register_user(session, user)
    
    return {
        'id': new_user.id,
        'username': new_user.username,
        'privilegio': new_user.privilegio
    }


@router.post(
        '/login',
        status_code=status.HTTP_200_OK,
        response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = crud_user.get_user_by_username(session, user.username.lower())

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail='Senha incorreta')

    access_token = create_access_token(
        {
            'sub': db_user.username, 
            'id': db_user.id,
            'privilegio': db_user.privilegio.nome
        }
    )
    refresh_token = create_refresh_token(
        {
            'sub': db_user.username,
            'id': db_user.id
        }
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }


@router.post('/refresh')
def refresh_token(request: TokenRefreshRequest, session: Session = Depends(get_session)):
    payload = verify_token(request.refresh_token)
    db_user = crud_user.get_user_by_username(session, payload.get('sub'))
    new_access_token = create_access_token(
        {
            'sub': db_user.username,
            'id': db_user.id, 
            'privilegio': db_user.privilegio.nome
        }
    )

    return {'access_token': new_access_token, 'token_type': 'bearer'}
