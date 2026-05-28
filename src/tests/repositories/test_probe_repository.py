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
    probe = Probe(x=0, y=0, direction="N")

    # Act
    saved_probe = await repository.save(probe)

    # Assert
    mock_session.add.assert_called_once_with(probe)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(probe)
    assert saved_probe == probe


@pytest.mark.asyncio
async def test_probe_repository_get_by_id():
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
    # Arrange
    mock_session = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    repository = ProbeRepository(session=mock_session)
    probe = Probe(x=0, y=0, direction="N")

    # Act
    updated_probe = await repository.update(probe)

    # Assert
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(probe)
    assert updated_probe == probe
