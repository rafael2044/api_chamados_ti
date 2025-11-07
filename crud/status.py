from sqlalchemy.orm import Session
from sqlalchemy import select

from models.status import Status

class CRUDStatus:

    def get_status(self, session: Session) -> list[Status]:
        status = session.scalars(select(Status)).all()
        return status
    
crud_status = CRUDStatus()