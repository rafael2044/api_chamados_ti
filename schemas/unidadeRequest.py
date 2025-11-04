from pydantic import BaseModel, ConfigDict


class UnidadeRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    nome: str
