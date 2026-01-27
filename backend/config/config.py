from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    DATABASE_HOST: str = Field(default="localhost", alias="PGHOST")
    DATABASE_PORT: int = Field(default=5432, alias="PGPORT")
    DATABASE_USER: str = Field(default="postgres", alias="PGUSER")
    DATABASE_PASSWORD: str = Field(default="password", alias="PGPASSWORD")
    DATABASE_NAME: str = Field(default="iot_hydroponik", alias="PGDATABASE")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: str = Field(default="1h", alias="JWT_EXPIRES_IN")  # 60 minutes
    SECRET_KEY: str = Field(default="mysecretkey", alias="JWT_SECRET")
    SUPERUSER_USERNAME: str = Field(default="admin", alias="SUPERUSER_USERNAME")
    SUPERUSER_EMAIL: str = Field(default="admin@example.com", alias="SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD: str = Field(default="adminpassword", alias="SUPERUSER_PASSWORD")
    SUPERUSER_ROLE: str = Field(default="superadmin", alias="SUPERUSER_ROLE")
    

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


settings = Settings()
