from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app


@pytest.mark.anyio
async def test_health_check():
    """Deve retornar um status de saúde saudável."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.anyio
async def test_launch_probe_success():
    """Uma sonda sempre começará no canto inferior esquerdo da malha, representado pelas coordenadas (0,0)."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/v1/launch-probe", json={"x": 0, "y": 0, "direction": "NORTH"}
        )
    assert response.status_code == 201


@pytest.mark.anyio
async def test_launch_probe_invalid_direction():
    """Deve lançar um erro se ele tentar passar uma direção inválida."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/v1/launch-probe", json={"x": 0, "y": 0, "direction": "UP"}
        )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_launch_probe_invalid_coordinates_type():
    """Deverá lançar um erro se ele tentar passar strings nas coordenadas x ou y."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/v1/launch-probe",
            json={"x": "invalid_x", "y": "invalid_y", "direction": "NORTH"},
        )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_launch_probe_empty_payload():
    """Deverá lançar um erro se ele não passar nada no corpo da requisição."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/api/v1/launch-probe", json={})
    assert response.status_code == 422
