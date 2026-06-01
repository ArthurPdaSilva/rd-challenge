from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.core.exceptions import (
    BusinessException,
    GridNotFoundException,
    GridSizeInvalidException,
    InvalidCommandException,
    InvalidMovementException,
    ProbeNotFoundException,
)
from app.schemas.probe import (
    ProbeLaunch,
    ProbeMove,
    ProbeResponse,
    ProbesPositionsResponse,
)
from app.services.probe_service import ProbeService

router = APIRouter()


@router.get("/", tags=["health"])
async def health_check():
    return {"message": "API de Controle de Sondas no Planeta Marte está funcionando!"}


def _raise_http_from_business_exception(exc: BusinessException) -> None:
    """Converte exceções de negócio em HTTPExceptions apropriadas."""

    if isinstance(exc, ProbeNotFoundException):
        raise HTTPException(status_code=404, detail=exc.message) from exc
    if isinstance(exc, (GridSizeInvalidException, InvalidCommandException)):
        raise HTTPException(status_code=422, detail=exc.message) from exc
    if isinstance(exc, GridNotFoundException):
        raise HTTPException(status_code=404, detail=exc.message) from exc
    if isinstance(exc, InvalidMovementException):
        raise HTTPException(status_code=409, detail=exc.message) from exc

    raise HTTPException(status_code=400, detail=exc.message) from exc


@router.post("/probes", response_model=ProbeResponse, status_code=201, tags=["probe"])
async def launch_probe(
    probe: ProbeLaunch,
    session: SessionDep,
):
    """Lança uma sonda em uma malha e retorna os dados iniciais da sonda."""

    probe_service = ProbeService(session)
    try:
        launched_probe = await probe_service.launch_probe(probe)
        return {
            "id": launched_probe.id,
            "x": launched_probe.x,
            "y": launched_probe.y,
            "direction": launched_probe.direction,
        }
    except BusinessException as e:
        _raise_http_from_business_exception(e)


@router.post(
    "/probes/{probe_id}/commands",
    response_model=ProbeResponse,
    status_code=200,
    tags=["probe"],
)
async def move_probe(
    probe_id: int,
    move_probe: ProbeMove,
    session: SessionDep,
):
    """Aplica comandos de movimento (M, L, R) em uma sonda existente."""
    probe_service = ProbeService(session)
    try:
        moved_probe = await probe_service.move_probe(probe_id, move_probe)
        return {
            "id": moved_probe.id,
            "x": moved_probe.x,
            "y": moved_probe.y,
            "direction": moved_probe.direction,
        }
    except BusinessException as e:
        _raise_http_from_business_exception(e)


@router.get("/probes", response_model=ProbesPositionsResponse, tags=["probe"])
async def see_probe_positions(session: SessionDep):
    """Retorna a lista com as posições de todas as sondas lançadas."""
    probe_service = ProbeService(session)
    positions_response = await probe_service.see_probe_positions()
    return positions_response
