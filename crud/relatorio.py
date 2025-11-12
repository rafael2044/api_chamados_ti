from sqlalchemy import select, func
from sqlalchemy.orm import Session


from datetime import datetime
from models.chamado import Chamado
from models.modulo import Modulo
from models.status import Status
from models.unidade import Unidade

class QueryRelatorio:

    def get_relatorio_chamados_por_modulo(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):
        query = (select(Modulo.nome, func.count(Chamado.id).label('total'))
                 .join(Modulo, Chamado.modulo_id == Modulo.id, isouter=True))
        
        if data_inicio:
            query = query.where(Chamado.data_abertura >= data_inicio)

        if data_fim:
            query = query.where(Chamado.data_abertura <= data_fim)

        query = (query
                 .group_by(Modulo.nome)
                 .order_by(func.count(Chamado.id).desc())
            )

        return session.execute(query).mappings().all()
    

    def get_relatorio_tmr_por_modulo(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):

        diferenca_em_segundos = func.extract(
        'epoch', (Chamado.data_fechamento - Chamado.data_abertura)
        )

        media_em_horas = func.avg(diferenca_em_segundos / 3600).label("tempo_medio")

        query = (select(Modulo.nome, media_em_horas)
                 .join(Modulo, Chamado.modulo_id == Modulo.id, isouter=True))
        
        query = query.where(Chamado.data_fechamento.is_not(None))
        
        if data_inicio:
            query = query.where(Chamado.data_abertura >= data_inicio)

        if data_fim:
            query = query.where(Chamado.data_abertura <= data_fim)

        query = (query
                 .group_by(Modulo.nome)
                 .order_by(media_em_horas.desc())
            )

        return session.execute(query).mappings().all()
    
    def get_relatorio_chamados_por_status(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):

        query = (
        select(
            Status.nome.label("nome"),
            func.count(Chamado.id).label("total")
        )
        .join(Status, Chamado.status_id == Status.id) 
        )

        if data_inicio:
            query = query.where(Chamado.data_abertura >= data_inicio)
        if data_fim:
            query = query.where(Chamado.data_abertura <= data_fim)

        query = (
            query
            .group_by(Status.nome)
            .order_by(func.count(Chamado.id).desc())
        )

        result = session.execute(query).mappings().all()
    
        return result
    
    def get_relatorio_chamados_por_unidade(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):

        query = (
        select(
            Unidade.nome.label("nome"),
            func.count(Chamado.id).label("total")
        )
        .join(Unidade, Chamado.unidade_id == Unidade.id) 
        )

        if data_inicio:
            query = query.where(Chamado.data_abertura >= data_inicio)
        if data_fim:
            query = query.where(Chamado.data_abertura <= data_fim)

        query = (
            query
            .group_by(Unidade.nome)
            .order_by(func.count(Chamado.id).desc())
        )

        result = session.execute(query).mappings().all()
    
        return result
    
query_relatorio = QueryRelatorio()