from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")

    username: str
    password: str
    privilegio: int
