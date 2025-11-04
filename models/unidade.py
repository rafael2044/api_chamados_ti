from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.database import Base
from models.chamado import Chamado


class Unidade(Base):
    __tablename__ = 'unidade'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    chamados: Mapped[List['Chamado']] = relationship(back_populates='unidade')
