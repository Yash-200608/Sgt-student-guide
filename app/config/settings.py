import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    database_name: str = Field(default="sgt_navigator")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)
    allow_admin_signup: bool = Field(default=False)


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_name=os.getenv("DATABASE_NAME", "sgt_navigator"),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
        allow_admin_signup=os.getenv("ALLOW_ADMIN_SIGNUP", "false").lower() == "true",
    )


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is required.")
    return value
