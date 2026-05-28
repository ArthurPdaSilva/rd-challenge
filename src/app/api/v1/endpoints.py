# Lançar sonda e Configurar malha

from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.schemas.probe import ProbeLaunch, ProbeMove, ProbeResponse
from app.services.probe_service import ProbeService

router = APIRouter()


@router.get("/health-check", tags=["health"])
async def health_check():
    """Verificar a saúde da aplicação."""
    return {"status": "healthy"}


@router.post(
    "/launch-probe", response_model=ProbeResponse, status_code=201, tags=["probe"]
)
async def launch_probe(
    probe: ProbeLaunch,
    session: SessionDep,
):

    probe_service = ProbeService(session)
    try:
        launched_probe = await probe_service.launch_probe(probe)
        return {
            "id": launched_probe.id,
            "x": launched_probe.x,
            "y": launched_probe.y,
            "direction": launched_probe.direction,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post(
    "/move-probe", response_model=ProbeResponse, status_code=200, tags=["probe"]
)
async def move_probe(
    move_probe: ProbeMove,
    session: SessionDep,
):
    probe_service = ProbeService(session)
    try:
        moved_probe = await probe_service.move_probe(move_probe)
        return {
            "id": moved_probe.id,
            "x": moved_probe.x,
            "y": moved_probe.y,
            "direction": moved_probe.direction,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
