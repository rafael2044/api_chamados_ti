from sqlalchemy.orm import Session
from sqlalchemy import select

from models.privilegio import Privilegio

class CRUDPrivilegio:

    def get_privilegios(self, session: Session) -> list[Privilegio]:
        smtm = select(Privilegio).order_by(Privilegio.id);
        privilegios = session.scalars(smtm).all()
        return privilegios
    
crud_privilegio = CRUDPrivilegio()