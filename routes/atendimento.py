import os
from http import HTTPStatus
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from core.security import JWTBearer, get_current_user, require_privilegio
from db.database import get_session
from models.user import User
from schemas.atendimentoResponse import AtendimentoResponse
from crud.atendimento import crud_atendimento as crud


router = APIRouter(prefix='/atendimento', tags=['Atendimento'])

TARGET_TIMEZONE = ZoneInfo("America/Sao_Paulo")


@router.post(
    '/{chamado_id}',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador', 'Suporte']))],
    response_model=AtendimentoResponse,
    status_code=HTTPStatus.OK
)
async def insert_atendimento(
    chamado_id: int,
    descricao: str = Form(...),
    anexo: UploadFile | None = File(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_atendimento = crud.insert_atendimento(
        session, descricao, chamado_id, current_user.id, anexo)
    return {
        'id': new_atendimento.id,
        'suporte': current_user.username,
        'descricao': new_atendimento.descricao,
        'data_atendimento': new_atendimento.data_atendimento.astimezone(TARGET_TIMEZONE),
        'url_anexo': new_atendimento.url_anexo
    }

    