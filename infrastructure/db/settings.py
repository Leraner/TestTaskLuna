from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres"
    port: int = 5432
    host: str = "database"
    dialect: str = "postgresql"
    driver: str = "asyncpg"

    @property
    def connection_url(self) -> str:
        return (
            f"{self.dialect}+{self.driver}:"
            f"//{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.db}"
        )

    model_config = SettingsConfigDict(env_prefix="POSTGRES", validate_assignment=True)
