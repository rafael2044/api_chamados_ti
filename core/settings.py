from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str
    SECRET_KEY: str
    CLOUD_NAME: str
    CLOUD_API_KEY: str
    CLOUD_SECRET_KEY: str
    CLIENT_ORIGINS: str
    PATH_SSL_CERT: str
    PATH_SSL_KEY: str
    PATH_SSL_ROOT_CERT: str

    @property
    def ORIGINS_AS_LIST(self) -> List[str]:
        if not self.CLIENT_ORIGINS:
            return []
        
        return [origin.strip() for origin in self.CLIENT_ORIGINS.split(',')]