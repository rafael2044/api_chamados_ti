from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.database import Base
from models.user import User


class Privilegio(Base):
    __tablename__ = 'privilegio'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    usuarios: Mapped[List['User']] = relationship(back_populates='privilegio')
