from pydantic import BaseModel, ConfigDict


class UserLogin(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    username: str
    password: str
