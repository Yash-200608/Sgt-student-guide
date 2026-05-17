import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://sgt-student-guide.vercel.app",
]


def _parse_csv_env(name: str) -> list[str]:
    value = os.getenv(name, "")
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseModel):
    database_name: str = Field(default="sgt_navigator")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)
    allow_admin_signup: bool = Field(default=False)
    cors_origins: list[str] = Field(default_factory=list)
    cors_origin_regex: str | None = Field(default=r"https://.*\.vercel\.app")


@lru_cache
def get_settings() -> Settings:
    configured_origins = _parse_csv_env("CORS_ORIGINS")
    return Settings(
        database_name=os.getenv("DATABASE_NAME", "sgt_navigator"),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
        allow_admin_signup=os.getenv("ALLOW_ADMIN_SIGNUP", "false").lower() == "true",
        cors_origins=[*DEFAULT_CORS_ORIGINS, *configured_origins],
        cors_origin_regex=os.getenv("CORS_ORIGIN_REGEX", r"https://.*\.vercel\.app"),
    )


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is required.")
    return value


def get_mongodb_url() -> str:
    mongodb_url = os.getenv("MONGODB_URL")
    if mongodb_url:
        return mongodb_url

    legacy_mongo_url = os.getenv("MONGO_URL")
    if legacy_mongo_url:
        return legacy_mongo_url

    raise RuntimeError("MONGODB_URL environment variable is required.")
