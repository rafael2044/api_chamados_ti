from pydantic import BaseModel, ConfigDict


class ChamadoRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    titulo: str
    unidade: int
    setor: str
    modulo: int
    urgencia: str
    descricao: str
