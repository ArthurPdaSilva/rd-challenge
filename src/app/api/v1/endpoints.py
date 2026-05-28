# Lançar sonda e Configurar malha

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas.probe import ProbeLaunch, ProbeLaunchResponse
from app.services.probe_service import ProbeService

router = APIRouter()


@router.get("/health-check", tags=["health"])
async def health_check():
    """Verificar a saúde da aplicação."""
    return {"status": "healthy"}


@router.post(
    "/launch-probe", response_model=ProbeLaunchResponse, status_code=201, tags=["probe"]
)
async def launch_probe(
    probe: ProbeLaunch,
    session: SessionDep,
):

    probe_service = ProbeService(session)
    launched_probe = await probe_service.launch_probe(probe)

    return {
        "id": launched_probe.id,
        "x": launched_probe.x,
        "y": launched_probe.y,
        "direction": launched_probe.direction,
    }
