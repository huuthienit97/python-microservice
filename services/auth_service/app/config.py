from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ARANGO_URL: str = "http://arangodb:8529"
    ARANGO_DB: str = "auth_service_db"
    ARANGO_ROOT_PASSWORD: str = "rootpassword"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
