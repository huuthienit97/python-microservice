from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ARANGO_URL: str = "http://arangodb:8529"
    ARANGO_DB: str = "product_service_db"
    ARANGO_ROOT_PASSWORD: str = "rootpassword"

    class Config:
        env_file = ".env"
