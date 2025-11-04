from pydantic import BaseModel, ConfigDict


class TokenRefreshRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    refresh_token: str
