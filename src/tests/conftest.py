from unittest.mock import AsyncMock, MagicMock

from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app
from app.models.grid import Grid
from app.models.probe import Probe


@pytest.fixture
async def async_client():
    """Fixture para fornecer um cliente HTTP assíncrono para os testes."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def mock_session():
    """Fixture para injetar um mock da sessão de banco de dados nas camadas de repositório e serviços."""
    session = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.exec = AsyncMock()
    return session


@pytest.fixture
def mock_grid():
    """Fixture que retorna uma malha 5x5 padrão."""
    return Grid(dimension_x=5, dimension_y=5)


@pytest.fixture
def mock_probe(mock_grid):
    """Fixture que retorna uma sonda em 0,0 virada NORTH na malha mock."""
    return Probe(id=1, x=0, y=0, direction="NORTH", grid=mock_grid)
