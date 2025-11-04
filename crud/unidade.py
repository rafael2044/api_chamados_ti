from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from http import HTTPStatus


from schemas.unidadeRequest import UnidadeRequest
from models.unidade import Unidade


class CRUDUnidade:


    def get_unidades(
            self,
            session: Session,
            offset: int = 1,
            limit: int = 100,
            search: str = ''
    ) -> list[Unidade]:
        skip = (offset - 1) * limit
        smtm = select(Unidade).offset(skip).limit(limit)
        if search:
            smtm = (select(Unidade)
                    .where(Unidade.nome.ilike(f'%{search}%'))
                    .offset(skip)
                    .limit(limit))
        
        return session.scalars(smtm).all()


    def get_total_unidades(self, session: Session, search: str = '') -> int:
        smtm = select(Unidade)
        if search:
            smtm = (select(Unidade).where(Unidade.nome.ilike(f'%{search}%')))

        total = session.execute(select(func.count()).select_from(smtm)).scalar()
        return total


    def get_unidade_by_id(self, session: Session, unidade_id: int) -> Unidade:
        unidade_db = session.scalars(
            select(Unidade)
            .where(Unidade.id == unidade_id)
        ).first()
        if not unidade_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Unidade não existe'
            )

        return unidade_db
    

    def exists_unidade(self, session: Session, nome: str) -> bool:
        unidade_db = session.scalars(
            select(Unidade)
            .where(Unidade.nome == nome)).first()
        if not unidade_db:
            return False
        return True


    def insert_unidade(self, session: Session, unidade: UnidadeRequest) -> Unidade:
        if self.exists_unidade(session, unidade.nome):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Unidade já existe'
            )
        new_unidade = Unidade(nome = unidade.nome)
        session.add(new_unidade)
        session.commit()
        session.refresh(new_unidade)
        return new_unidade


    def delete_unidade(self, session:Session, unidade_id: int):
        unidade_db = self.get_unidade_by_id(session, unidade_id)
        
        session.delete(unidade_db)
        session.commit()


crud_unidade = CRUDUnidade()