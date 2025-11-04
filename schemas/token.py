from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'