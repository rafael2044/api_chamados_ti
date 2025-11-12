from fastapi import APIRouter, Depends, status as HTTPStatus
from sqlalchemy.orm import Session


from core.security import JWTBearer, require_privilegio
from db.database import get_session
from schemas.moduloRequest import ModuloRequest
from schemas.moduloResponse import ModuloResponse
from schemas.modulosResponse import ModulosResponse
from crud.modulo import crud_modulo as crud


router = APIRouter(prefix='/modulo', tags=['Modulo'])


@router.get(
    '/',
    dependencies=[Depends(JWTBearer())],
    response_model=ModulosResponse,
    status_code=HTTPStatus.HTTP_200_OK
)
def get_modulos(
    session: Session = Depends(get_session),
    offset: int = 1,
    limit: int = 100,
    search: str = ''):

    result = []
    modulos = crud.get_modulos(session, offset=offset, limit=limit, search=search)
    total = crud.get_total_modulos(session, search)

    for m in modulos:
        result.append(ModuloResponse.model_validate(m))

    return {
        'modulos': result,
        'total': total,
        'offset': offset,
        'limit': limit,
        'total_pages': (total + limit - 1) // limit
    }


@router.post(
    '/',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador', 'Suporte']))],
    response_model=ModuloResponse,
    status_code=HTTPStatus.HTTP_201_CREATED
)
def create_modulo(
        modulo: ModuloRequest,
        session: Session = Depends(get_session),
):
    new_modulo = crud.insert_modulo(session, modulo)

    return ModuloResponse.model_validate(new_modulo)


@router.delete(
    '/{modulo_id}',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador', 'Suporte']))],
    status_code=HTTPStatus.HTTP_204_NO_CONTENT
)
def delete_modulo(modulo_id: int, session: Session = Depends(get_session)):
    crud.delete_modulo(session, modulo_id)

