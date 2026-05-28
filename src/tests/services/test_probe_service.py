from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.probe import ProbeLaunch
from app.services.probe_service import ProbeService


@pytest.mark.asyncio
async def test_launch_probe():
    # Arrange
    mock_session = AsyncMock()
    launch_request = ProbeLaunch(x=5, y=5, direction="NORTH")

    with patch("app.services.probe_service.ProbeRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value

        # O repositório irá retornar este probe mockado ao ser salvo
        mock_saved_probe = MagicMock()
        mock_saved_probe.id = 1
        mock_saved_probe.direction = "NORTH"

        # Simula o método assíncrono save()
        mock_repo_instance.save = AsyncMock(return_value=mock_saved_probe)

        service = ProbeService(session=mock_session)

        # Act
        response = await service.launch_probe(launch_request)

        # Assert
        MockRepo.assert_called_once_with(mock_session)
        mock_repo_instance.save.assert_awaited_once()

        # Validando os campos retornados no Response
        assert response.id == 1
        assert response.x == 5
        assert response.y == 5
        assert response.direction == "NORTH"
