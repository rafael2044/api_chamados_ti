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
from schemas.chamadoResponse import ChamadoResponse


router = APIRouter(prefix='/chamados', tags=['Chamados'])
TARGET_TIMEZONE = ZoneInfo('America/Sao_Paulo')



@router.get(
    '/',
    response_model=ChamadosResponse,
    dependencies=[Depends(JWTBearer())],
    status_code=HTTPStatus.OK
)
def get_chamados(
    session: Session = Depends(get_session),
    offset: int = 1,
    limit: int = 10,
    search: str = '',
    unidade_id: int = None,
    modulo_id: int = None,
    status_id: int = None,
    urgencia: str = ''
):
    chamados = crud.get_chamados(
        session, 
        offset, 
        limit,
        search,
        unidade_id,
        modulo_id,
        status_id,
        urgencia)
    
    total = crud.get_total_chamados(
        session,
        search,
        unidade_id, 
        modulo_id,
        status_id, 
        urgencia)
    
    result = []
    for c in chamados:
        result.append({
            'id': c.id,
            'titulo': c.titulo,
            'unidade': c.unidade.nome if c.unidade else '',
            'setor': c.setor,
            'modulo': c.modulo.nome if c.modulo else '',
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


@router.patch(
        '/{chamado_id}',
        dependencies= [
            Depends(JWTBearer()),
            Depends(require_privilegio(['Administrador', 'Suporte']))
        ],
        response_model=ChamadoResponse,
        status_code=HTTPStatus.OK
)
def update_chamado(
    chamado_id:int,
    chamado_update: ChamadoRequest,
    session: Session = Depends(get_session)
):
    chamado_db = crud.update_chamado(
            session, 
            chamado_id, 
            {
                'titulo': chamado_update.titulo,
                'unidade_id': chamado_update.unidade,
                'setor': chamado_update.setor,
                'modulo_id': chamado_update.modulo,
                'urgencia': chamado_update.urgencia,
                'descricao': chamado_update.descricao 
            }
        )

    return {
            'id': chamado_db.id,
            'titulo': chamado_db.titulo,
            'unidade': chamado_db.unidade.nome if chamado_db.unidade else '',
            'setor': chamado_db.setor,
            'modulo': chamado_db.modulo.nome if chamado_db.modulo else '',
            'urgencia': chamado_db.urgencia,
            'descricao': chamado_db.descricao,
            'status': chamado_db.status.nome,
            'url_anexo': chamado_db.url_anexo,
            'data_abertura': chamado_db.data_abertura.astimezone(TARGET_TIMEZONE),
            'data_fechamento': chamado_db.data_fechamento.astimezone(TARGET_TIMEZONE) if chamado_db.data_fechamento else None,
            'solicitante': chamado_db.usuario.username if chamado_db.usuario else 'Desconhecido',
            'atendimentos': [
                {
                    'id': a.id,
                    'descricao': a.descricao,
                    'data_atendimento': a.data_atendimento.astimezone(TARGET_TIMEZONE),
                    'suporte': a.suporte.username if a.suporte else 'Desconhecido',
                    'url_anexo': a.url_anexo
                }
                for a in (chamado_db.atendimentos or [])
            ]
        }


@router.delete(
    '/{chamado_id}',
    dependencies=[Depends(JWTBearer()), Depends(require_privilegio(['Administrador', 'Suporte']))],
    status_code=HTTPStatus.NO_CONTENT
)
def delete_chamado(chamado_id: int, session: Session = Depends(get_session)):
    crud.delete_chamado(session, chamado_id)
