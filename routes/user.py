from fastapi import APIRouter, Depends, status as HTTPStatus
from sqlalchemy.orm import Session


from core.security import JWTBearer, require_privilegio
from db.database import get_session
from schemas.userCreate import UserCreate
from schemas.usersResponse import UsersResponse
from schemas.userResponse import UserResponse
from crud.user import crud_user as crud


router = APIRouter(prefix='/user', tags=['User'])


@router.get(
    '/',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador']))],
    response_model=UsersResponse,
    status_code=HTTPStatus.HTTP_200_OK
)
def get_users(
    offset: int = 1,
    limit: int = 10,
    search: str = '',
    session: Session = Depends(get_session)
):
    
    skip = (offset - 1) * limit
    users = crud.get_users(session, skip, limit, search)
    total = crud.get_total_users(session, search)
    result = []
    for u in users:
        result.append({
            'id': u.id,
            'username': u.username,
            'privilegio': u.privilegio
        })
    
    return {
        'users': result,
        'total': total,
        'offset': offset,
        'limit': limit,
        'total_pages': (total + limit - 1) // limit
    }


@router.post(
    '/',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador']))],
    response_model= UserResponse,
    status_code=HTTPStatus.HTTP_201_CREATED
)
def create_user(
        user: UserCreate,
        session: Session = Depends(get_session),
):
    new_user = crud.insert_user(session, user)
    
    return {
        'id': new_user.id,
        'username': new_user.username,
        'privilegio': new_user.privilegio
    }


@router.patch(
        '/reset-password/{user_id}',
        dependencies=[Depends(JWTBearer()), Depends(require_privilegio('Administrador'))],
        status_code=HTTPStatus.HTTP_200_OK
)
def update_password(user_id: int, password: str, session: Session = Depends(get_session)):
    user_db = crud.update_password(session, user_id, password)

    return {
        'message': 'Senha alterada',
        'user_id': user_db.id
    }


@router.delete(
    '/{user_id}',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador']))],
    status_code=HTTPStatus.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    crud.delete_user(session, user_id)