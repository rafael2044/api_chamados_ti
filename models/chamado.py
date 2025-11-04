from datetime import datetime
from typing import List
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.database import Base


class Chamado(Base):
    __tablename__ = 'chamado'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    unidade_id: Mapped[int] = mapped_column(
        ForeignKey('unidade.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    setor: Mapped[str] = mapped_column(String(75), nullable=False)
    modulo_id: Mapped[int] = mapped_column(
        ForeignKey('modulo.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True
    )
    urgencia: Mapped[str] = mapped_column(String(20), nullable=False)
    descricao: Mapped[str] = mapped_column(Text(), nullable=False)
    status_id: Mapped[int] = mapped_column(
        ForeignKey('status.id'),
        nullable=False)
    data_abertura: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now()
    )
    data_fechamento: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    url_anexo: Mapped[str] = mapped_column(nullable=True)

    unidade: Mapped['Unidade'] = relationship(back_populates='chamados')
    modulo: Mapped['Modulo'] = relationship(back_populates='chamados')
    usuario: Mapped['User'] = relationship(back_populates='chamados')
    status: Mapped['Status'] = relationship(back_populates='chamados')
    atendimentos: Mapped[List['Atendimento']] = relationship(
        back_populates='chamado')


from models.atendimento import Atendimento
from models.unidade import Unidade
from models.modulo import Modulo
from models.user import User
from models.status import Status
