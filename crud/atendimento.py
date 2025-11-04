from sqlalchemy import select, func
from sqlalchemy.orm import Session 
from fastapi import HTTPException, UploadFile, File
from http import HTTPStatus
import cloudinary.uploader

from models.atendimento import Atendimento
from crud.chamado import crud_chamado


class CRUDAtendimento:

    def get_atendimentos(
            self,
            session: Session,
            offset: int = 1,
            limit: int = 100,
            search: str = ''
    ) -> list[Atendimento]:
        skip = (offset - 1) * limit
        smtm = select(Atendimento).offset(skip).limit(limit)
        if search:
            smtm = (select(Atendimento)
                    .where(Atendimento.nome.ilike(f'%{search}%'))
                    .offset(skip)
                    .limit(limit))
        
        return session.scalars(smtm).all()


    def get_total_atendimentos(self, session: Session, search: str = '') -> int:
        smtm = select(Atendimento)
        if search:
            smtm = (select(Atendimento).where(Atendimento.descricao.ilike(f'%{search}%')))

        total = session.execute(select(func.count()).select_from(smtm)).scalar()
        return total


    def get_atendimento_by_id(self, session: Session, atendimento_id: int) -> Atendimento:
        atendimento_db = session.scalars(
            select(Atendimento)
            .where(Atendimento.id == atendimento_id)
        ).first()
        if not atendimento_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Unidade não existe'
            )

        return atendimento_db


    def exists_atendimento(self, session: Session, descricao: str) -> bool:
        atendimento_db = session.scalars(
            select(Atendimento)
            .where(Atendimento.descricao == descricao)).first()
        if not atendimento_db:
            return False
        return True


    def insert_atendimento(
            self, session: Session,
            descricao: str,
            chamado_id: int, 
            suporte_id: int,
            anexo: UploadFile | None = File(None)
    ) -> Atendimento:
        chamado_db = crud_chamado.get_chamado_by_id(session, chamado_id)
        if chamado_db.status_id != 3:
            new_atendimento = Atendimento(
                descricao=descricao,
                chamado_id=chamado_db.id,
                suporte_id=suporte_id,
            )
            if anexo:
                try:
                    upload_result: dict = cloudinary.uploader.upload(
                        anexo.file,
                        resource_type='auto',
                        type="upload",
                        folder="anexo_atendimentos",
                        use_filename=True,
                        unique_filename=True
                    )

                    url_anexo = upload_result.get("secure_url")

                    new_atendimento.url_anexo = url_anexo

                except Exception as e:
                    raise HTTPException(
                        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                        detail='Erro no sistema de upload'
                    )
            crud_chamado.update_chamado(session, chamado_id, {"status_id": 2})
            session.add(new_atendimento)
            session.commit()
            session.refresh(new_atendimento)
            return new_atendimento
        else:   
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="O chamado já está finalizado!"
            )
       

crud_atendimento = CRUDAtendimento()