from pydantic import BaseModel, ConfigDict



class ModuloRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    nome: str
