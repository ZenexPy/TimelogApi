from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "secret" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "secret" / "jwt-public.pem"

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    auth_jwt: AuthJWT = AuthJWT()

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DATABASE_URL_psycopg(self):
        # DSN
        # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
