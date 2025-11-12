from pydantic import BaseModel, ConfigDict
from typing import List


from schemas.unidadeResponse import UnidadeResponse


class UnidadesResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    unidades: List[UnidadeResponse]
    total: int
    limit: int
    offset: int
    total_pages: int