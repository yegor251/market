from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str = "postgres"
    db_password: str = "qwerty"
    db_name: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()