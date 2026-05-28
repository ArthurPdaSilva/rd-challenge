from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.grid import Grid
from app.models.probe import Probe
from app.repositories.grid_repository import GridRepository
from app.repositories.probe_repository import ProbeRepository
from app.schemas.probe import (
    DirectionEnum,
    ProbeLaunch,
    ProbeMove,
    ProbeResponse,
    ProbesPositionsResponse,
)


class ProbeService:
    def __init__(self, session: AsyncSession):
        self.repository = ProbeRepository(session)
        self.grid_repository = GridRepository(session)
        self.valid_directions = {"NORTH", "EAST", "SOUTH", "WEST"}

    async def launch_probe(self, probe: ProbeLaunch) -> ProbeResponse:
        if probe.x <= 0 or probe.y <= 0:
            raise ValueError("O tamanho da malha deve ser maior que zero.")

        grid_dimension = Grid(dimension_x=probe.x, dimension_y=probe.y)

        probe = Probe(x=0, y=0, direction=probe.direction.upper(), grid=grid_dimension)

        launched_probe = await self.repository.save(probe)

        return ProbeResponse(
            id=launched_probe.id,
            x=grid_dimension.dimension_x,
            y=grid_dimension.dimension_y,
            direction=launched_probe.direction,
        )

    async def see_probe_positions(self) -> ProbesPositionsResponse:
        probes = await self.repository.get_all()
        return ProbesPositionsResponse(
            probes=[
                ProbeResponse(id=p.id, x=p.x, y=p.y, direction=p.direction)
                for p in probes
            ]
        )

    async def move_probe(self, moveProbe: ProbeMove) -> Probe:
        probe = await self.repository.get_by_id(moveProbe.id)
        if not probe:
            raise ValueError("Sonda não encontrada.")

        cmd = moveProbe.command.upper()

        if not all(c in "LRM" for c in cmd):
            raise ValueError("Comando inválido. Use apenas 'L', 'R' e 'M'.")

        grid = await self.grid_repository.get_by_probe_id(moveProbe.id)

        if not grid:
            raise ValueError("Malha associada à sonda não encontrada.")

        handlers = {
            "L": lambda: self._turn_left(probe),
            "R": lambda: self._turn_right(probe),
            "M": lambda: self._move_forward(probe, grid),
        }

        for c in cmd:
            handlers[c]()

        updated_probe = await self.repository.update(probe)
        return updated_probe

    def _turn_left(self, probe: Probe) -> None:
        directions = ["NORTH", "WEST", "SOUTH", "EAST"]
        probe.direction = self.get_next_direction(probe.direction, directions)

    def _turn_right(self, probe: Probe) -> None:
        directions = ["NORTH", "EAST", "SOUTH", "WEST"]
        probe.direction = self.get_next_direction(probe.direction, directions)

    def get_next_direction(self, direction: DirectionEnum, directions: list) -> str:
        current_index = directions.index(direction)
        return directions[(current_index + 1) % 4]

    def _move_forward(self, probe: Probe, grid: Grid):
        MOVES = {
            "NORTH": (0, 1),
            "EAST": (1, 0),
            "SOUTH": (0, -1),
            "WEST": (-1, 0),
        }
        move_x, move_y = MOVES[probe.direction]
        new_x = probe.x + move_x
        new_y = probe.y + move_y

        if (
            new_x < 0
            or new_x > grid.dimension_x
            or new_y < 0
            or new_y > grid.dimension_y
        ):
            raise ValueError("Movimento inválido. A sonda não pode sair da malha.")

        probe.x = new_x
        probe.y = new_y
