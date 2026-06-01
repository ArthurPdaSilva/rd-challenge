from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.grid import Grid


class GridRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_probe_id(self, probe_id: int):
        """Recupera a malha associada a uma sonda pelo ID da sonda."""
        statement = select(Grid).where(Grid.probe_id == probe_id)
        result = await self.session.exec(statement)
        return result.first()
