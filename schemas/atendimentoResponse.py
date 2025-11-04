from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class AtendimentoResponse(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    id: int
    suporte: str
    descricao: str
    data_atendimento: datetime
    url_anexo: Optional[str] = None
    
