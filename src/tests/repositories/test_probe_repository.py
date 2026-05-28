from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.probe import Probe
from app.repositories.probe_repository import ProbeRepository


@pytest.mark.asyncio
async def test_probe_repository_save():
    # Arrange
    mock_session = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    repository = ProbeRepository(session=mock_session)
    probe = Probe(x=0, y=0, direction="NORTH")

    # Act
    saved_probe = await repository.save(probe)

    # Assert
    mock_session.add.assert_called_once_with(probe)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(probe)
    assert saved_probe == probe


@pytest.mark.asyncio
async def test_probe_repository_get_by_id():
    """
    Deverá retornar a sonda com id 1.
    """

    # Arrange
    mock_session = MagicMock()
    mock_session.get = AsyncMock()
    repository = ProbeRepository(session=mock_session)

    # Act
    await repository.get_by_id(1)

    # Assert
    mock_session.get.assert_awaited_once_with(Probe, 1)


@pytest.mark.asyncio
async def test_probe_repository_update():
    """Deverá atualizar a sonda com id 1 para a posição (1,0) virada para EAST."""

    # Arrange
    mock_session = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    repository = ProbeRepository(session=mock_session)
    probe = Probe(x=0, y=0, direction="NORTH")

    # Act
    updated_probe = await repository.update(probe)

    # Assert
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(probe)
    assert updated_probe == probe


@pytest.mark.asyncio
async def test_probe_repository_get_all():
    """Deverá retornar todas as sondas cadastradas."""

    # Arrange
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_probe1 = Probe(x=0, y=0, direction="NORTH")
    mock_probe2 = Probe(x=1, y=1, direction="EAST")
    mock_result.scalars().all.return_value = [mock_probe1, mock_probe2]
    mock_session.exec.return_value = mock_result
    repository = ProbeRepository(session=mock_session)

    # Act
    result = await repository.get_all()

    # Assert
    mock_session.exec.assert_awaited_once()
    assert result == [mock_probe1, mock_probe2]
