from unittest.mock import MagicMock

import pytest

from app.models.probe import Probe
from app.repositories.probe_repository import ProbeRepository


@pytest.mark.asyncio
async def test_probe_repository_save(mock_session, mock_probe):
    # Arrange
    repository = ProbeRepository(session=mock_session)

    # Act
    saved_probe = await repository.save(mock_probe)

    # Assert
    mock_session.add.assert_called_once_with(mock_probe)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(mock_probe)
    assert saved_probe == mock_probe


@pytest.mark.asyncio
async def test_probe_repository_get_by_id(mock_session):
    """
    Deverá retornar a sonda com id 1.
    """
    # Arrange
    repository = ProbeRepository(session=mock_session)

    # Act
    await repository.get_by_id(1)

    # Assert
    mock_session.get.assert_awaited_once_with(Probe, 1)


@pytest.mark.asyncio
async def test_probe_repository_update(mock_session, mock_probe):
    """Deverá atualizar a sonda com id 1 para a posição (1,0) virada para EAST."""
    # Arrange
    repository = ProbeRepository(session=mock_session)

    # Act
    updated_probe = await repository.update(mock_probe)

    # Assert
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(mock_probe)
    assert updated_probe == mock_probe


@pytest.mark.asyncio
async def test_probe_repository_get_all(mock_session, mock_probe):
    """Deverá retornar todas as sondas cadastradas."""
    # Arrange
    mock_result = MagicMock()
    mock_probe2 = Probe(x=1, y=1, direction="EAST")
    mock_result.all.return_value = [mock_probe, mock_probe2]
    mock_session.exec.return_value = mock_result
    repository = ProbeRepository(session=mock_session)

    # Act
    result = await repository.get_all()

    # Assert
    mock_session.exec.assert_awaited_once()
    assert result == [mock_probe, mock_probe2]
