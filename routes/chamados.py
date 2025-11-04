from http import HTTPStatus
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo


from core.security import JWTBearer, get_current_user, require_privilegio
from db.database import get_session
from models.user import User
from crud.chamado import crud_chamado as crud
from schemas.chamadoRequest import ChamadoRequest
from schemas.chamadosResponse import ChamadosResponse


router = APIRouter(prefix='/chamados', tags=['Chamados'])
TARGET_TIMEZONE = ZoneInfo('America/Sao_Paulo')



@router.get(
    '/',
    response_model=ChamadosResponse,
    dependencies=[Depends(JWTBearer())],
    status_code=HTTPStatus.OK
)
def get_chamados(session: Session = Depends(get_session), offset: int = 1, limit: int = 10, search: str = ''):
    chamados = crud.get_chamados(session, offset=offset, limit=limit, search=search)
    total = crud.get_total_chamados(session, search=search)
    result = []
    for c in chamados:
        result.append({
            'id': c.id,
            'titulo': c.titulo,
            'unidade': c.unidade.nome if c.unidade else '———',
            'setor': c.setor,
            'modulo': c.modulo.nome if c.modulo else '———',
            'urgencia': c.urgencia,
            'descricao': c.descricao,
            'status': c.status.nome,
            'url_anexo': c.url_anexo,
            'data_abertura': c.data_abertura.astimezone(TARGET_TIMEZONE),
            'data_fechamento': c.data_fechamento.astimezone(TARGET_TIMEZONE) if c.data_fechamento else None,
            'solicitante': c.usuario.username if c.usuario else 'Desconhecido',
            'atendimentos': [
                {
                    'id': a.id,
                    'descricao': a.descricao,
                    'data_atendimento': a.data_atendimento.astimezone(TARGET_TIMEZONE),
                    'suporte': a.suporte.username if a.suporte else 'Desconhecido',
                    'url_anexo': a.url_anexo
                }
                for a in (c.atendimentos or [])
            ]
        })
    return {
        'chamados': result,
        'total': total,
        'offset': offset,
        'limit': limit,
        'total_pages': (total + limit - 1) // limit
        }


@router.post(
    '/',
    dependencies=[Depends(JWTBearer())],
    status_code=HTTPStatus.CREATED
)
def create_chamado(
    chamado: ChamadoRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_chamado = crud.insert_chamado(session, chamado, current_user.id)
    return {'chamado_id': new_chamado.id, 'message': f'Chamado #{new_chamado.id} aberto com sucesso'}


@router.post('/{chamado_id}/anexo', dependencies=[Depends(JWTBearer())], status_code=HTTPStatus.CREATED)
async def upload_anexo_chamado(
    chamado_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    await crud.insert_anexo_chamado(session, file, chamado_id)

    return {'message': 'Arquivo enviado com sucesso'}


@router.patch(
        '/{chamado_id}/finalizar',
        dependencies=[Depends(JWTBearer()),
                    Depends(require_privilegio(['Administrador', 'Suporte']))],
        status_code=HTTPStatus.OK
              )
def finalizar_chamado(chamado_id: int,
                      session: Session = Depends(get_session)):
    
    chamado_db= crud.finalizar_chamado(session, chamado_id)

    return {
        'message': f'Chamado #{chamado_id} finalizado com sucesso',
        'data_fechamento': chamado_db.data_fechamento.astimezone(TARGET_TIMEZONE)
    }
