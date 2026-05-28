from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.grid import Grid
from app.models.probe import Probe
from app.repositories.probe_repository import ProbeRepository
from app.schemas.probe import ProbeLaunch, ProbeLaunchResponse


class ProbeService:
    def __init__(self, session: AsyncSession):
        self.repository = ProbeRepository(session)

    async def launch_probe(self, probe: ProbeLaunch) -> ProbeLaunchResponse:
        grid_dimension = Grid(dimension_x=probe.x, dimension_y=probe.y)

        probe = Probe(x=0, y=0, direction=probe.direction.upper(), grid=grid_dimension)

        launched_probe = await self.repository.save(probe)

        return ProbeLaunchResponse(
            id=launched_probe.id,
            x=grid_dimension.dimension_x,
            y=grid_dimension.dimension_y,
            direction=launched_probe.direction,
        )
