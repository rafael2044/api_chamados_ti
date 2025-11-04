from pydantic import BaseModel


class ReportSLAItem(BaseModel):
    nome: str
    tempo_medio: float

    class Config:
        from_attributes = True