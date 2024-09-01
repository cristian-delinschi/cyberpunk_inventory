import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    # database
    DATABASE_URL = "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
        DB_USER=os.getenv("DB_USER", "fastapi"),
        DB_PASSWORD=os.getenv("DB_PASSWORD", "fastapi-password"),
        DB_HOST=os.getenv("DB_HOST", "fastapi-postgresql:5432"),
        DB_NAME=os.getenv("DB_NAME", "fastapi"),
    )


settings = Settings()
