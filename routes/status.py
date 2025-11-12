from fastapi import APIRouter, Depends, status as HTTPStatus
from sqlalchemy.orm import Session
from typing import List


from core.security import JWTBearer
from db.database import get_session
from schemas.statusResponse import StatusResponse
from crud.status import crud_status as crud


router = APIRouter(prefix='/status', tags=['Status'])


@router.get(
    '/',
    dependencies=[Depends(JWTBearer())],
    response_model=List[StatusResponse],
    status_code=HTTPStatus.HTTP_200_OK
)
def get_privilegios(session: Session = Depends(get_session)):
    status = crud.get_status(session)
    result = []
    for s in status:
        result.append(StatusResponse.model_validate(s))

    return result
