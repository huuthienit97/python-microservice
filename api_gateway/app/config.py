from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_SERVICE_URL: str = "http://user_service:8001"
    AUTH_SERVICE_URL: str = "http://auth_service:8002"
    PRODUCT_SERVICE_URL: str = "http://product_service:8003"

    class Config:
        env_file = ".env"
