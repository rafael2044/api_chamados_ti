from pydantic import BaseModel, ConfigDict
from typing import List


from schemas.moduloResponse import ModuloResponse


class ModulosResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    modulos: List[ModuloResponse]
    total: int
    limit: int
    offset: int
    total_pages: int