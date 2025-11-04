from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.database import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    privilegio_id: Mapped[int] = mapped_column(ForeignKey('privilegio.id'), nullable=False)

    privilegio: Mapped['Privilegio'] = relationship(
        back_populates='usuarios')
    chamados: Mapped[List['Chamado']] = relationship(
        back_populates='usuario')
    atendimentos: Mapped[List['Atendimento']] = relationship(
        back_populates='suporte')


from models.atendimento import Atendimento
from models.chamado import Chamado
from models.privilegio import Privilegio