from unittest.mock import MagicMock

import pytest

from app.repositories.grid_repository import GridRepository


@pytest.mark.asyncio
async def test_grid_repository_get_by_probe_id(mock_session, mock_grid):
    """
    Deverá retornar a malha associada à sonda com id 1.
    """
    # Arrange
    mock_result = MagicMock()
    mock_grid.probe_id = 1
    mock_result.first.return_value = mock_grid
    mock_session.exec.return_value = mock_result

    repository = GridRepository(session=mock_session)

    # Act
    result = await repository.get_by_probe_id(1)

    # Assert
    mock_session.exec.assert_awaited_once()
    assert result == mock_grid
