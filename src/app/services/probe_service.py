from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.grid import Grid
from app.models.probe import Probe
from app.repositories.probe_repository import ProbeRepository
from app.schemas.probe import ProbeLaunch, ProbeMove, ProbeResponse


class ProbeService:
    def __init__(self, session: AsyncSession):
        self.repository = ProbeRepository(session)
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

    async def move_probe(self, moveProbe: ProbeMove) -> Probe:
        probe = await self.repository.get_by_id(moveProbe.id)
        if not probe:
            raise ValueError("Sonda não encontrada.")

        cmd = moveProbe.command.upper()

        if not all(c in "LRM" for c in cmd):
            raise ValueError("Comando inválido. Use apenas 'L', 'R' e 'M'.")

        for c in cmd:
            if c == "L":
                probe.direction = self._turn_left(probe.direction)
            elif c == "R":
                probe.direction = self._turn_right(probe.direction)
            elif c == "M":
                self._move_forward(probe)

        updated_probe = await self.repository.update(probe)
        return updated_probe

    def _turn_left(self, direction: str) -> str:
        directions = ["NORTH", "WEST", "SOUTH", "EAST"]
        return self.get_next_direction(direction, directions)

    def _turn_right(self, direction: str) -> str:
        directions = ["NORTH", "EAST", "SOUTH", "WEST"]
        return self.get_next_direction(direction, directions)

    def get_next_direction(self, direction, directions):
        current_index = directions.index(direction)
        return directions[(current_index + 1) % 4]

    def _move_forward(self, probe: Probe):
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
            or new_x > probe.grid.dimension_x
            or new_y < 0
            or new_y > probe.grid.dimension_y
        ):
            raise ValueError("Movimento inválido. A sonda não pode sair da malha.")

        probe.x += new_x
        probe.y += new_y
