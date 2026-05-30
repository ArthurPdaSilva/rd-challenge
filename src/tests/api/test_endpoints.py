from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.exceptions import (
    InvalidCommandException,
    ProbeNotFoundException,
)
from app.schemas.probe import ProbesPositionsResponse


@pytest.mark.anyio
async def test_health_check(async_client):
    """Deve retornar um status de saúde saudável."""
    response = await async_client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "API de Controle de Sondas no Planeta Marte está funcionando!"
    }


@pytest.mark.anyio
async def test_launch_probe_success(async_client):
    """Uma sonda sempre começará no canto inferior esquerdo da malha, representado pelas coordenadas (0,0)."""
    with patch("app.api.v1.endpoints.ProbeService") as MockService:
        instance = MockService.return_value

        mock_launched = MagicMock()
        mock_launched.id = 1
        mock_launched.x = 5
        mock_launched.y = 5
        mock_launched.direction = "NORTH"
        instance.launch_probe = AsyncMock(return_value=mock_launched)
        response = await async_client.post(
            "/api/v1/launch-probe", json={"x": 5, "y": 5, "direction": "NORTH"}
        )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["x"] == 5
    assert data["y"] == 5
    assert data["direction"] == "NORTH"


@pytest.mark.anyio
async def test_launch_probe_invalid_direction(async_client):
    """Deve lançar um erro se ele tentar passar uma direção inválida."""
    response = await async_client.post(
        "/api/v1/launch-probe", json={"x": 0, "y": 0, "direction": "UP"}
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_launch_probe_invalid_coordinates_type(async_client):
    """Deverá lançar um erro se ele tentar passar strings nas coordenadas x ou y."""
    response = await async_client.post(
        "/api/v1/launch-probe",
        json={"x": "invalid_x", "y": "invalid_y", "direction": "NORTH"},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_launch_probe_empty_payload(async_client):
    """Deverá lançar um erro se ele não passar nada no corpo da requisição."""
    response = await async_client.post("/api/v1/launch-probe", json={})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_launch_probe_value_error(async_client):
    """Deverá retornar erro 400 se a grid for inválida (ex: x=0, y=0) tratada pelas exceções de negócio."""
    response = await async_client.post(
        "/api/v1/launch-probe", json={"x": 0, "y": 0, "direction": "NORTH"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "O tamanho da malha deve ser maior que zero."


@pytest.mark.anyio
async def test_move_probe_success(async_client):
    """Deverá mover a sonda com sucesso validando as novas coordenadas e direção."""
    with patch("app.api.v1.endpoints.ProbeService") as MockService:
        instance = MockService.return_value

        mock_moved = MagicMock()
        mock_moved.id = 1
        mock_moved.x = 1
        mock_moved.y = 0
        mock_moved.direction = "EAST"
        instance.move_probe = AsyncMock(return_value=mock_moved)
        move_resp = await async_client.post(
            "/api/v1/move-probe/1", json={"command": "RM"}
        )

        assert move_resp.status_code == 200

        data = move_resp.json()
        assert data["id"] == 1
        assert data["x"] == 1
        assert data["y"] == 0
        assert data["direction"] == "EAST"


@pytest.mark.anyio
async def test_move_probe_not_found(async_client):
    """Deverá retornar erro 400 se a sonda não existir."""
    with patch("app.api.v1.endpoints.ProbeService") as MockService:
        instance = MockService.return_value
        instance.move_probe = AsyncMock(side_effect=ProbeNotFoundException())
        response = await async_client.post(
            "/api/v1/move-probe/9999", json={"command": "M"}
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Sonda não encontrada."


@pytest.mark.anyio
async def test_move_probe_value_error(async_client):
    """Deverá retornar erro 400 se o comando for inválido."""
    with patch("app.api.v1.endpoints.ProbeService") as MockService:
        instance = MockService.return_value
        instance.move_probe = AsyncMock(side_effect=InvalidCommandException())
        response = await async_client.post(
            "/api/v1/move-probe/1", json={"command": "XYZ"}
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Comando inválido. Use apenas 'L', 'R' e 'M'."


@pytest.mark.anyio
async def test_see_probe_positions_success(async_client):
    """Deverá retornar a lista com as posições de todas as sondas lançadas."""
    with patch("app.api.v1.endpoints.ProbeService") as MockService:
        instance = MockService.return_value

        mock_positions_response = ProbesPositionsResponse(
            probes=[
                {"id": 1, "x": 1, "y": 2, "direction": "NORTH"},
                {"id": 2, "x": 3, "y": 4, "direction": "SOUTH"},
            ]
        )

        instance.see_probe_positions = AsyncMock(return_value=mock_positions_response)
        response = await async_client.get("/api/v1/probes")

    assert response.status_code == 200

    data = response.json()
    assert data == {
        "probes": [
            {"id": 1, "x": 1, "y": 2, "direction": "NORTH"},
            {"id": 2, "x": 3, "y": 4, "direction": "SOUTH"},
        ]
    }
