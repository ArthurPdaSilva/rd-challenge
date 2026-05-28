from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
import pytest

from app.main import lifespan


@pytest.mark.asyncio
async def test_lifespan():
    app_mock = FastAPI()
    
    with patch("app.main.init_db", new_callable=AsyncMock) as mock_init_db:
        async with lifespan(app_mock):
            # Assert that init_db was called during startup
            mock_init_db.assert_awaited_once()
