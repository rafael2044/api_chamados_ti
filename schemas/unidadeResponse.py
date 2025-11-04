from pydantic import BaseModel, ConfigDict


class UnidadeResponse(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)
    
    id: int
    nome: str