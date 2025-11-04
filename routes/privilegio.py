from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List


from core.security import JWTBearer, require_privilegio
from db.database import get_session
from schemas.privilegioResponse import PrivilegioResponse
from crud.privilegios import crud_privilegio as crud


router = APIRouter(prefix='/privilegio', tags=['Privilegio'])


@router.get(
    '/',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador', 'Suporte']))],
    response_model=List[PrivilegioResponse]
)
def get_privilegios(session: Session = Depends(get_session)):
    privilegios = crud.get_privilegios(session)
    result = []
    for p in privilegios:
        result.append(PrivilegioResponse.model_validate(p))

    return result
