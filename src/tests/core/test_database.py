from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlmodel import SQLModel

from app.core.database import get_session, init_db


@pytest.mark.asyncio
async def test_init_db():
    """Deverá criar as tabelas do banco de dados usando SQLModel.metadata.create_all."""

    # Arrange
    with patch("app.core.database.async_engine") as mock_engine:
        mock_conn = AsyncMock()
        mock_engine.begin.return_value.__aenter__.return_value = mock_conn
        mock_engine.begin.return_value.__aexit__.return_value = False

        # Act
        await init_db()

        # Assert
        mock_conn.run_sync.assert_awaited_once_with(SQLModel.metadata.create_all)


@pytest.mark.asyncio
async def test_get_session():
    """Deverá criar uma sessão de banco de dados usando sessionmaker e retorná-la."""

    # Arrange
    with patch("app.core.database.sessionmaker") as mock_sessionmaker:
        mock_session_instance = AsyncMock()
        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__.return_value = (
            mock_session_instance
        )
        mock_session_factory.return_value.__aexit__.return_value = False

        mock_sessionmaker.return_value = mock_session_factory

        # Act & Assert
        async for session in get_session():
            assert session == mock_session_instance
            break

        mock_sessionmaker.assert_called_once()
