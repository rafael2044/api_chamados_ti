from pydantic import BaseModel, ConfigDict
from typing import List


from schemas.chamadoResponse import ChamadoResponse


class ChamadosResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    chamados: List[ChamadoResponse]
    total: int
    offset: int
    limit: int
    total_pages: int