# Lançar sonda e Configurar malha

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas.probe import ProbeCreate

router = APIRouter()


@router.get("/health-check", tags=["health"])
async def health_check():
    """Verificar a saúde da aplicação."""
    return {"status": "healthy"}


@router.post("/launch-probe", status_code=201, tags=["probe"])
async def launch_probe(
    probe: ProbeCreate,
    session: SessionDep,
):
    """Lançar uma sonda e definir a grid de operação."""
    print(session)

    return {
        "id": "abc123",
        "x": 0,
        "y": 0,
        "direction": probe.direction.upper(),
    }
