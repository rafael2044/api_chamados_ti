from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from http import HTTPStatus


from schemas.moduloRequest import ModuloRequest
from models.modulo import Modulo


class CRUDModulo:


    def get_modulos(
            self,
            session: Session,
            offset: int = 1,
            limit: int = 100,
            search: str = ''
    ) -> list[Modulo]:
        skip = (offset - 1) * limit
        smtm = select(Modulo).offset(skip).limit(limit).order_by(Modulo.id)
        if search:
            smtm = (select(Modulo)
                    .where(Modulo.nome.ilike(f'%{search}%'))
                    .offset(skip)
                    .limit(limit)
                    .order_by(Modulo.id))
        
        return session.scalars(smtm).all()


    def get_total_modulos(self, session: Session, search: str = ''):
        smtm = select(Modulo)
        if search:
            smtm = (select(Modulo).where(Modulo.nome.ilike(f'%{search}%')))

        total = session.execute(select(func.count()).select_from(smtm)).scalar()
        return total


    def get_modulo_by_id(self, session: Session, modulo_id: int) -> Modulo:
        modulo_db = session.scalars(
            select(Modulo)
            .where(Modulo.id == modulo_id)
        ).first()
        if not modulo_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Modulo não existe'
            )

        return modulo_db


    def exists_modulo(self, session: Session, nome: str) -> bool:
        modulo_db = session.scalars(
            select(Modulo)
            .where(Modulo.nome == nome)).first()
        if not modulo_db:
            return False
        return True


    def insert_modulo(self, session: Session, modulo: ModuloRequest) -> Modulo:
        if self.exists_modulo(session, modulo.nome):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Modulo já existe'
            )
        new_modulo = Modulo(nome = modulo.nome)
        session.add(new_modulo)
        session.commit()
        session.refresh(new_modulo)
        return new_modulo


    def delete_modulo(self, session:Session, modulo_id: int):
        modulo_db = self.get_modulo_by_id(session, modulo_id)
        
        session.delete(modulo_db)
        session.commit()
        


crud_modulo = CRUDModulo()