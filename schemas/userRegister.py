from pydantic import BaseModel, ConfigDict


class UserRegister(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    username: str
    password: str
