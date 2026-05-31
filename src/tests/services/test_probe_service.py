from unittest.mock import AsyncMock, MagicMock, patch

from pydantic_core import ValidationError
import pytest

from app.core.exceptions import (
    GridNotFoundException,
    GridSizeInvalidException,
    InvalidCommandException,
    InvalidMovementException,
    ProbeNotFoundException,
)
from app.schemas.probe import ProbeLaunch, ProbeMove, ProbeResponse
from app.services.probe_service import ProbeService


@pytest.mark.asyncio
async def test_launch_probe(mock_session, mock_probe):
    """Deverá lançar uma sonda com sucesso e retornar seus dados iniciais."""

    # Arrange
    launch_request = ProbeLaunch(x=5, y=5, direction="NORTH")

    with patch("app.services.probe_service.ProbeRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value

        mock_repo_instance.save = AsyncMock(return_value=mock_probe)

        service = ProbeService(session=mock_session)

        # Act
        response = await service.launch_probe(launch_request)

        # Assert
        MockRepo.assert_called_once_with(mock_session)
        mock_repo_instance.save.assert_awaited_once()
        assert response.id == mock_probe.id
        assert response.x == mock_probe.x
        assert response.y == mock_probe.y
        assert response.direction == mock_probe.direction


@pytest.mark.asyncio
async def test_launch_probe_invalid_grid(mock_session):
    """Deverá retornar erro 400 se a grid for inválida (ex: x=0, y=0) tratada pelo GridSizeInvalidException."""

    # Arrange
    launch_request = ProbeLaunch(x=-1, y=5, direction="NORTH")
    service = ProbeService(session=mock_session)

    # Act & Assert
    with pytest.raises(GridSizeInvalidException) as exc_info:
        await service.launch_probe(launch_request)

    assert str(exc_info.value) == "O tamanho da malha deve ser maior que zero."


@pytest.mark.asyncio
async def test_launch_probe_invalid_direction(mock_session):
    """Deverá retornar erro de validação (ValidationError) se a direção for inválida."""
    # Arrange (N/A)

    # Act & Assert
    with pytest.raises(ValidationError):
        ProbeLaunch(x=5, y=5, direction="INVALIDA")


@pytest.mark.asyncio
async def test_move_probe_not_found(mock_session):
    """Deverá levantar ProbeNotFoundException se a sonda não for encontrada no banco de dados."""
    # Arrange
    move_req = ProbeMove(command="M")

    with patch("app.services.probe_service.ProbeRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id = AsyncMock(return_value=None)

        service = ProbeService(session=mock_session)

        # Act & Assert
        with pytest.raises(ProbeNotFoundException) as exc_info:
            await service.move_probe(99, move_req)
        assert str(exc_info.value) == "Sonda não encontrada."


@pytest.mark.asyncio
async def test_move_probe_invalid_command(mock_session):
    """Deverá levantar InvalidCommandException se o comando de movimento contiver caracteres inválidos."""
    # Arrange
    move_req = ProbeMove(command="XYZ")

    with patch("app.services.probe_service.ProbeRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id = AsyncMock(return_value=MagicMock())

        service = ProbeService(session=mock_session)

        # Act & Assert
        with pytest.raises(InvalidCommandException) as exc_info:
            await service.move_probe(1, move_req)
        assert str(exc_info.value) == "Comando inválido. Use apenas 'L', 'R' e 'M'."


@pytest.mark.asyncio
async def test_move_probe_empty_command(mock_session):
    """Deverá levantar InvalidCommandException se o comando de movimento for vazio ou contiver apenas espaços."""
    # Arrange
    move_req = ProbeMove(command="   ")

    with patch("app.services.probe_service.ProbeRepository") as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.get_by_id = AsyncMock(return_value=MagicMock())

        service = ProbeService(session=mock_session)

        # Act & Assert
        with pytest.raises(InvalidCommandException) as exc_info:
            await service.move_probe(1, move_req)
        assert str(exc_info.value) == "Comando inválido. Use apenas 'L', 'R' e 'M'."


@pytest.mark.asyncio
async def test_move_probe_grid_not_found(mock_session):
    """Deverá levantar GridNotFoundException se a malha associada à sonda não for encontrada."""
    # Arrange
    move_req = ProbeMove(command="M")

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
        with pytest.raises(GridNotFoundException) as exc_info:
            await service.move_probe(1, move_req)
        assert str(exc_info.value) == "Malha associada à sonda não encontrada."


@pytest.mark.asyncio
async def test_move_probe_success(mock_session, mock_probe):
    """Deverá mover a sonda com sucesso ao longo da malha utilizando comandos válidos."""
    # Arrange
    move_req = ProbeMove(command="RML")

    with (
        patch("app.services.probe_service.ProbeRepository") as MockRepo,
        patch("app.services.probe_service.GridRepository") as MockGridRepo,
    ):
        mock_repo_instance = MockRepo.return_value
        mock_grid_repo_instance = MockGridRepo.return_value

        mock_repo_instance.get_by_id = AsyncMock(return_value=mock_probe)
        mock_repo_instance.update = AsyncMock(return_value=mock_probe)
        mock_grid_repo_instance.get_by_probe_id = AsyncMock(
            return_value=mock_probe.grid
        )

        service = ProbeService(session=mock_session)

        # Act
        updated_probe = await service.move_probe(1, move_req)

        # Assert
        assert updated_probe.direction == "NORTH"
        assert updated_probe.x == 1
        assert updated_probe.y == 0
        mock_repo_instance.update.assert_awaited_once_with(mock_probe)


@pytest.mark.asyncio
async def test_move_probe_mrm_success(mock_session, mock_probe):
    """Deverá mover a sonda da posição (0,0) utilizando 'MRM' e parar em (1,1) virada para EAST."""
    # Arrange
    move_req = ProbeMove(command="MRM")

    with (
        patch("app.services.probe_service.ProbeRepository") as MockRepo,
        patch("app.services.probe_service.GridRepository") as MockGridRepo,
    ):
        mock_repo_instance = MockRepo.return_value
        mock_grid_repo_instance = MockGridRepo.return_value

        mock_repo_instance.get_by_id = AsyncMock(return_value=mock_probe)
        mock_repo_instance.update = AsyncMock(return_value=mock_probe)
        mock_grid_repo_instance.get_by_probe_id = AsyncMock(
            return_value=mock_probe.grid
        )

        service = ProbeService(session=mock_session)

        # Act
        updated_probe = await service.move_probe(1, move_req)

        # Assert
        assert updated_probe.x == 1
        assert updated_probe.y == 1
        assert updated_probe.direction == "EAST"
        mock_repo_instance.update.assert_awaited_once_with(mock_probe)


@pytest.mark.asyncio
async def test_see_probe_positions(mock_session):
    """Deverá retornar sondas lançadas e suas posições atuais."""
    # Arrange

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


@pytest.mark.parametrize(
    "initial_x, initial_y, direction",
    [
        (5, 5, "NORTH"),  # Sai pelo topo
        (5, 5, "EAST"),  # Sai pela direita
        (0, 0, "SOUTH"),  # Sai por baixo
        (0, 0, "WEST"),  # Sai pela esquerda
    ],
)
@pytest.mark.asyncio
async def test_move_probe_out_of_bounds(
    mock_session, mock_probe, initial_x, initial_y, direction
):
    """Deverá levantar InvalidMovementException se a sonda tentar se mover para fora dos limites em qualquer direção."""
    # Arrange
    move_req = ProbeMove(command="M")

    with (
        patch("app.services.probe_service.ProbeRepository") as MockRepo,
        patch("app.services.probe_service.GridRepository") as MockGridRepo,
    ):
        mock_repo_instance = MockRepo.return_value
        mock_grid_repo_instance = MockGridRepo.return_value

        # Sonda na borda correspondente virada para a direção especificada tentando avançar
        mock_probe.x = initial_x
        mock_probe.y = initial_y
        mock_probe.direction = direction
        mock_repo_instance.get_by_id = AsyncMock(return_value=mock_probe)
        mock_grid_repo_instance.get_by_probe_id = AsyncMock(
            return_value=mock_probe.grid
        )

        service = ProbeService(session=mock_session)

        # Act & Assert
        with pytest.raises(InvalidMovementException) as exc_info:
            await service.move_probe(1, move_req)
        assert (
            str(exc_info.value) == "Movimento inválido. A sonda não pode sair da malha."
        )


@pytest.mark.parametrize(
    "command, initial_direction",
    [
        ("LLLL", "NORTH"),  # 4x esquerda, continua NORTH
        ("RRRR", "NORTH"),  # 4x direita, continua NORTH
    ],
)
@pytest.mark.asyncio
async def test_move_probe_full_turn(
    mock_session, mock_probe, command, initial_direction
):
    """Deverá manter a direção inicial após dar uma volta completa para qualquer lado (4x L ou 4x R)."""
    # Arrange
    move_req = ProbeMove(command=command)

    with (
        patch("app.services.probe_service.ProbeRepository") as MockRepo,
        patch("app.services.probe_service.GridRepository") as MockGridRepo,
    ):
        mock_repo_instance = MockRepo.return_value
        mock_grid_repo_instance = MockGridRepo.return_value

        mock_probe.direction = initial_direction
        mock_repo_instance.get_by_id = AsyncMock(return_value=mock_probe)
        mock_repo_instance.update = AsyncMock(return_value=mock_probe)
        mock_grid_repo_instance.get_by_probe_id = AsyncMock(
            return_value=mock_probe.grid
        )

        service = ProbeService(session=mock_session)

        # Act
        updated_probe = await service.move_probe(1, move_req)

        # Assert
        assert updated_probe.direction == initial_direction
        mock_repo_instance.update.assert_awaited_once_with(mock_probe)
