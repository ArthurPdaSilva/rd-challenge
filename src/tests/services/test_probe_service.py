from unittest.mock import AsyncMock, MagicMock, patch

from pydantic_core import ValidationError
import pytest

from app.models.grid import Grid
from app.models.probe import Probe
from app.schemas.probe import ProbeLaunch, ProbeMove, ProbeResponse
from app.services.probe_service import ProbeService


@pytest.mark.asyncio
async def test_launch_probe():
    """Deverá lançar uma sonda com sucesso e retornar seus dados iniciais."""

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


@pytest.mark.asyncio
async def test_launch_probe_invalid_grid():
    """Deverá retornar erro 400 se a grid for inválida (ex: x=0, y=0) tratada pelo ValueError."""

    # Arrange
    mock_session = AsyncMock()
    launch_request = ProbeLaunch(x=-1, y=5, direction="NORTH")
    service = ProbeService(session=mock_session)

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await service.launch_probe(launch_request)

    assert str(exc_info.value) == "O tamanho da malha deve ser maior que zero."


@pytest.mark.asyncio
async def test_launch_probe_invalid_direction():
    """Deverá retornar erro de validação (ValidationError) se a direção for inválida."""
    # Arrange (N/A)

    # Act & Assert
    with pytest.raises(ValidationError):
        ProbeLaunch(x=5, y=5, direction="INVALIDA")


@pytest.mark.asyncio
async def test_move_probe_not_found():
    """Deverá levantar ValueError se a sonda não for encontrada no banco de dados."""
    # Arrange
    mock_session = AsyncMock()
    move_req = ProbeMove(id=99, command="M")

    with patch("app.services.probe_service.ProbeRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id = AsyncMock(return_value=None)

        service = ProbeService(session=mock_session)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await service.move_probe(move_req)
        assert str(exc_info.value) == "Sonda não encontrada."


@pytest.mark.asyncio
async def test_move_probe_invalid_command():
    """Deverá levantar ValueError se o comando de movimento contiver caracteres inválidos."""
    # Arrange
    mock_session = AsyncMock()
    move_req = ProbeMove(id=1, command="XYZ")

    with patch("app.services.probe_service.ProbeRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id = AsyncMock(return_value=MagicMock())

        service = ProbeService(session=mock_session)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await service.move_probe(move_req)
        assert str(exc_info.value) == "Comando inválido. Use apenas 'L', 'R' e 'M'."


@pytest.mark.asyncio
async def test_move_probe_grid_not_found():
    """Deverá levantar ValueError se a malha associada à sonda não for encontrada."""
    # Arrange
    mock_session = AsyncMock()
    move_req = ProbeMove(id=1, command="M")

    with (
        patch("app.services.probe_service.ProbeRepository") as MockRepo,
        patch("app.services.probe_service.GridRepository") as MockGridRepo,
    ):
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id = AsyncMock(return_value=MagicMock())

        mock_grid_repo = MockGridRepo.return_value
        mock_grid_repo.get_by_probe_id = AsyncMock(return_value=None)

        service = ProbeService(session=mock_session)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await service.move_probe(move_req)
        assert str(exc_info.value) == "Malha associada à sonda não encontrada."


@pytest.mark.asyncio
async def test_move_probe_success():
    """Deverá mover a sonda com sucesso ao longo da malha utilizando comandos válidos."""
    # Arrange
    mock_session = AsyncMock()
    move_req = ProbeMove(id=1, command="RML")

    with (
        patch("app.services.probe_service.ProbeRepository") as MockRepo,
        patch("app.services.probe_service.GridRepository") as MockGridRepo,
    ):
        mock_repo_instance = MockRepo.return_value
        mock_grid_repo_instance = MockGridRepo.return_value

        mock_probe = Probe(
            x=0, y=0, direction="NORTH", grid=Grid(dimension_x=5, dimension_y=5)
        )
        mock_repo_instance.get_by_id = AsyncMock(return_value=mock_probe)
        mock_repo_instance.update = AsyncMock(return_value=mock_probe)
        mock_grid_repo_instance.get_by_probe_id = AsyncMock(
            return_value=mock_probe.grid
        )

        service = ProbeService(session=mock_session)

        # Act
        updated_probe = await service.move_probe(move_req)

        # Assert
        assert updated_probe.direction == "NORTH"
        assert updated_probe.x == 1
        assert updated_probe.y == 0
        mock_repo_instance.update.assert_awaited_once_with(mock_probe)


@pytest.mark.asyncio
async def test_move_probe_mrm_success():
    """Deverá mover a sonda da posição (0,0) utilizando 'MRM' e parar em (1,1) virada para EAST."""
    # Arrange
    mock_session = AsyncMock()
    move_req = ProbeMove(id=1, command="MRM")

    with (
        patch("app.services.probe_service.ProbeRepository") as MockRepo,
        patch("app.services.probe_service.GridRepository") as MockGridRepo,
    ):
        mock_repo_instance = MockRepo.return_value
        mock_grid_repo_instance = MockGridRepo.return_value

        mock_probe = Probe(
            x=0, y=0, direction="NORTH", grid=Grid(dimension_x=5, dimension_y=5)
        )
        mock_repo_instance.get_by_id = AsyncMock(return_value=mock_probe)
        mock_repo_instance.update = AsyncMock(return_value=mock_probe)
        mock_grid_repo_instance.get_by_probe_id = AsyncMock(
            return_value=mock_probe.grid
        )

        service = ProbeService(session=mock_session)

        # Act
        updated_probe = await service.move_probe(move_req)

        # Assert
        assert updated_probe.x == 1
        assert updated_probe.y == 1
        assert updated_probe.direction == "EAST"
        mock_repo_instance.update.assert_awaited_once_with(mock_probe)


@pytest.mark.asyncio
async def test_see_probe_positions():
    """Deverá retornar as posições de todas as sondas lançadas."""
    # Arrange
    mock_session = AsyncMock()

    with patch("app.services.probe_service.ProbeRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value

        mock_probes = [
            MagicMock(id=1, x=1, y=2, direction="NORTH"),
            MagicMock(id=2, x=3, y=4, direction="SOUTH"),
        ]

        mock_repo_instance.get_all = AsyncMock(return_value=mock_probes)

        service = ProbeService(session=mock_session)

        # Act
        response = await service.see_probe_positions()

        # Assert
        mock_repo_instance.get_all.assert_awaited_once()
        assert response.probes == [
            ProbeResponse(id=1, x=1, y=2, direction="NORTH"),
            ProbeResponse(id=2, x=3, y=4, direction="SOUTH"),
        ]


@pytest.mark.asyncio
async def test_move_probe_out_of_bounds():
    """Deverá levantar ValueError se a sonda tentar se mover para fora dos limites da malha."""
    # Arrange
    mock_session = AsyncMock()
    move_req = ProbeMove(id=1, command="M")

    with (
        patch("app.services.probe_service.ProbeRepository") as MockRepo,
        patch("app.services.probe_service.GridRepository") as MockGridRepo,
    ):
        mock_repo_instance = MockRepo.return_value
        mock_grid_repo_instance = MockGridRepo.return_value

        # Sonda na borda superior (5,5) virada para o NORTH e tentando avançar
        mock_probe = Probe(
            x=5, y=5, direction="NORTH", grid=Grid(dimension_x=5, dimension_y=5)
        )
        mock_repo_instance.get_by_id = AsyncMock(return_value=mock_probe)
        mock_grid_repo_instance.get_by_probe_id = AsyncMock(
            return_value=mock_probe.grid
        )

        service = ProbeService(session=mock_session)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await service.move_probe(move_req)
        assert (
            str(exc_info.value) == "Movimento inválido. A sonda não pode sair da malha."
        )
