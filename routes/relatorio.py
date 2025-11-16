from fastapi import APIRouter, Depends, status as HTTPStatus
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime


from core.security import JWTBearer, require_privilegio
from db.database import get_session
from schemas.ReportItem import ReportItem
from schemas.reportSLAItem import ReportSLAItem
from crud.relatorio import query_relatorio


router = APIRouter(prefix='/relatorio', tags=['Relatorio'])


@router.get(
    '/chamados-por-modulo',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador']))],
    response_model=List[ReportItem],
    status_code=HTTPStatus.HTTP_200_OK
)
def get_relatorio_chamados_por_modulo(
    session: Session = Depends(get_session),
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None):

    result = query_relatorio.get_relatorio_chamados_por_modulo(session, data_inicio, data_fim)

    return result



@router.get(
    '/chamados-por-unidade',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador']))],
    response_model=List[ReportItem],
    status_code=HTTPStatus.HTTP_200_OK
)
def get_relatorio_chamados_por_unidade(
    session: Session = Depends(get_session),
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None):

    result = query_relatorio.get_relatorio_chamados_por_unidade(session, data_inicio, data_fim)

    return result


@router.get(
    '/chamados-por-status',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador']))],
    response_model=List[ReportItem],
    status_code=HTTPStatus.HTTP_200_OK
)
def get_relatorio_chamados_por_status(
    session: Session = Depends(get_session),
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None):

    result = query_relatorio.get_relatorio_chamados_por_status(session, data_inicio, data_fim)

    return result


@router.get(
    '/tmr-por-modulo',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador']))],
    response_model=List[ReportSLAItem],
    status_code=HTTPStatus.HTTP_200_OK
)
def get_relatorio_tmr_por_modulo(
    session: Session = Depends(get_session),
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None):

    result = query_relatorio.get_relatorio_tmr_por_modulo(session, data_inicio, data_fim)

    return result


@router.get(
    '/tmr-por-unidade',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador']))],
    response_model=List[ReportSLAItem],
    status_code=HTTPStatus.HTTP_200_OK
)
def get_relatorio_tmr_por_modulo(
    session: Session = Depends(get_session),
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None):

    result = query_relatorio.get_relatorio_tmr_por_unidade(session, data_inicio, data_fim)

    return result