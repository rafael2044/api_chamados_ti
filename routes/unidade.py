from fastapi import APIRouter, Depends, status as HTTPStatus
from sqlalchemy.orm import Session
from typing import List


from core.security import JWTBearer, require_privilegio
from db.database import get_session
from schemas.unidadeRequest import UnidadeRequest
from schemas.unidadeResponse import UnidadeResponse
from schemas.unidadesResponse import UnidadesResponse
from crud.unidade import crud_unidade as crud


router = APIRouter(prefix='/unidade', tags=['Unidade'])


@router.get(
        '/',
        dependencies=[Depends(JWTBearer())],
        response_model=UnidadesResponse,
        status_code=HTTPStatus.HTTP_200_OK
)
def get_unidades(
    session: Session = Depends(get_session),
    offset: int = 1,
    limit: int = 100,
    search: str = ''):

    unidades = crud.get_unidades(session, offset, limit, search)
    total = crud.get_total_unidades(session, search)
    result = []
    for u in unidades:
        result.append(UnidadeResponse.model_validate(u))

    return {
        'unidades': result,
        'total': total,
        'offset': offset,
        'limit': limit,
        'total_pages': (total + limit - 1) // limit
    }


@router.post(
    '/',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador', 'Suporte']))],
    response_model=UnidadeResponse,
    status_code=HTTPStatus.HTTP_201_CREATED
)
def create_unidade(unidade: UnidadeRequest, session: Session = Depends(get_session)):
    new_unidade = crud.insert_unidade(session, unidade)
    
    return UnidadeResponse.model_validate(new_unidade)


@router.delete(
    '/{unidade_id}',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador', 'Suporte']))],
    status_code=HTTPStatus.HTTP_204_NO_CONTENT
)
def delete_unidade(unidade_id: int, session: Session = Depends(get_session)):
    crud.delete_unidade(session, unidade_id)

