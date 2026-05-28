import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "minha_senha")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "meu_banco")
    POSTGRES_PORT: int = 5432

    def DATABASE_URL(self) -> str:
        """Retorna a URL de conexão com o banco de dados PostgreSQL usando asyncpg."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
