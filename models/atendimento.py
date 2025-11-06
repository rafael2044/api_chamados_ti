from datetime import datetime
from sqlalchemy import ForeignKey, Text, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.database import Base
from models.user import User


class Atendimento(Base):
    __tablename__ = 'atendimentos'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chamado_id: Mapped[int] = mapped_column(ForeignKey(
        'chamado.id', ondelete='CASCADE'))
    suporte_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    url_anexo: Mapped[str] = mapped_column(nullable=True)
    data_atendimento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False
    )

    suporte: Mapped['User'] = relationship(back_populates='atendimentos')
    chamado: Mapped['Chamado'] = relationship(back_populates='atendimentos')

from models.chamado import Chamado