from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session


from datetime import datetime
from models.chamado import Chamado
from models.modulo import Modulo
from models.status import Status
from models.unidade import Unidade

class QueryRelatorio:

    def get_relatorio_chamados_por_modulo(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):
        # Cláusula ON básica
        join_on_clause = Modulo.id == Chamado.modulo_id

        # ---- A LÓGICA DO FILTRO ----

        # Verificamos se AMBAS as datas existem
        if data_inicio and data_fim:
            join_on_clause = and_(
                join_on_clause,
                # Aplicamos o BETWEEN aqui, na cláusula ON
                Chamado.data_abertura.between(data_inicio, data_fim)
            )
        elif data_inicio:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura >= data_inicio)
        elif data_fim:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura <= data_fim)

        # (Se o usuário passar só uma data, o filtro de data é ignorado)

        query = (
            select(
                Modulo.nome,
                func.count(Chamado.id).label('total')
            )
            .select_from(Modulo)
            .join(Chamado, join_on_clause, isouter=True)  # LEFT JOIN
            .group_by(Modulo.nome)
            .order_by(func.count(Chamado.id).desc())
        )

        return session.execute(query).mappings().all()
    

    def get_relatorio_tmr_por_modulo(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):

        diferenca_em_segundos = func.extract(
            'epoch', (Chamado.data_fechamento - Chamado.data_abertura)
        )
        # Usamos func.coalesce para mostrar 0 em vez de NULL se a média for nula
        media_em_horas = func.coalesce(
            func.avg(diferenca_em_segundos / 3600), 0
        ).label("tempo_medio")

        # 1. Começamos a cláusula ON básica
        join_on_clause = Modulo.id == Chamado.modulo_id

        # 2. Adicionamos TODOS os filtros do Chamado à cláusula ON

        # Filtro obrigatório para TMR (só calcula se estiver fechado)
        join_on_clause = and_(join_on_clause, Chamado.data_fechamento.is_not(None))

        # Filtros de data (lógica completa)
        if data_inicio and data_fim:
            join_on_clause = and_(
                join_on_clause,
                Chamado.data_abertura.between(data_inicio, data_fim)
            )
        elif data_inicio:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura >= data_inicio)
        elif data_fim:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura <= data_fim)

        # 3. Construção da Query
        query = (
            select(Modulo.nome, media_em_horas)
            .select_from(Modulo)  # Começa POR Modulo
            .join(Chamado, join_on_clause, isouter=True)  # LEFT JOIN com cláusula ON completa
            .group_by(Modulo.nome)
            .order_by(media_em_horas.desc())
        )

        return session.execute(query).mappings().all()


    def get_relatorio_tmr_por_unidade(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):

        diferenca_em_segundos = func.extract(
            'epoch', (Chamado.data_fechamento - Chamado.data_abertura)
        )
        # Usamos func.coalesce para mostrar 0 em vez de NULL se a média for nula
        media_em_horas = func.coalesce(
            func.avg(diferenca_em_segundos / 3600), 0
        ).label("tempo_medio")

        # 1. Começamos a cláusula ON básica
        join_on_clause = Unidade.id == Chamado.unidade_id

        # 2. Adicionamos TODOS os filtros do Chamado à cláusula ON

        # Filtro obrigatório para TMR (só calcula se estiver fechado)
        join_on_clause = and_(join_on_clause, Chamado.data_fechamento.is_not(None))

        # Filtros de data (lógica completa)
        if data_inicio and data_fim:
            join_on_clause = and_(
                join_on_clause,
                Chamado.data_abertura.between(data_inicio, data_fim)
            )
        elif data_inicio:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura >= data_inicio)
        elif data_fim:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura <= data_fim)

        # 3. Construção da Query
        query = (
            select(Unidade.nome, media_em_horas)
            .select_from(Unidade)  # Começa POR Unidade
            .join(Chamado, join_on_clause, isouter=True)  # LEFT JOIN com cláusula ON completa
            .group_by(Unidade.nome)
            .order_by(media_em_horas.desc())
        )

        return session.execute(query).mappings().all()

    def get_relatorio_chamados_por_status(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):

        join_on_clause = Status.id == Chamado.status_id

        # 2. Adiciona filtros de data à cláusula ON
        if data_inicio and data_fim:
            join_on_clause = and_(
                join_on_clause,
                Chamado.data_abertura.between(data_inicio, data_fim)
            )
        elif data_inicio:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura >= data_inicio)
        elif data_fim:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura <= data_fim)

        # 3. Construção da Query
        query = (
            select(
                Status.nome.label("nome"),
                func.count(Chamado.id).label("total")
            )
            .select_from(Status)  # Começa POR Status
            .join(Chamado, join_on_clause, isouter=True)  # LEFT JOIN
            .group_by(Status.nome)
            .order_by(func.count(Chamado.id).desc())
        )

        return session.execute(query).mappings().all()
    
    def get_relatorio_chamados_por_unidade(self, session: Session, data_inicio: datetime = None, data_fim: datetime = None):

        # 1. Cláusula ON básica
        join_on_clause = Unidade.id == Chamado.unidade_id

        # 2. Adiciona filtros de data à cláusula ON
        if data_inicio and data_fim:
            join_on_clause = and_(
                join_on_clause,
                Chamado.data_abertura.between(data_inicio, data_fim)
            )
        elif data_inicio:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura >= data_inicio)
        elif data_fim:
            join_on_clause = and_(join_on_clause,
                                  Chamado.data_abertura <= data_fim)

        # 3. Construção da Query
        query = (
            select(
                Unidade.nome.label("nome"),
                func.count(Chamado.id).label("total")
            )
            .select_from(Unidade)  # Começa POR Unidade
            .join(Chamado, join_on_clause, isouter=True)  # LEFT JOIN
            .group_by(Unidade.nome)
            .order_by(func.count(Chamado.id).desc())
        )

        return session.execute(query).mappings().all()
    
query_relatorio = QueryRelatorio()