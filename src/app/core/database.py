from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

database_url = settings.DATABASE_URL()

async_engine = create_async_engine(url=database_url, echo=True)


async def init_db():
    """Inicializa o banco de dados criando as tabelas definidas nos modelos."""
    async with async_engine.begin() as conn:
        """É necessário importar os modelos antes de criar as tabelas para garantir que eles sejam registrados no SQLModel.metadata."""
        from app.models.probe import Probe  # noqa: F401

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """Fornece uma sessão assíncrona para interagir com o banco de dados."""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
