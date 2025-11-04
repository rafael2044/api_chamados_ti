from pydantic import BaseModel

class ReportItem(BaseModel):
    nome: str
    total: int

    class Config:
        from_attributes = True