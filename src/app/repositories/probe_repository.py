from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.probe import Probe


class ProbeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, probe: Probe):
        """Salva uma nova sonda no banco de dados."""
        self.session.add(probe)
        await self.session.commit()
        await self.session.refresh(probe)
        return probe

    async def get_by_id(self, probe_id: int):
        """Recupera uma sonda pelo seu ID."""
        result = await self.session.get(Probe, probe_id)
        return result

    async def get_all(self):
        """Recupera todas as sondas do banco de dados."""
        result = await self.session.exec(select(Probe))
        return result.all()

    async def update(self, probe: Probe):
        """Atualiza uma sonda no banco de dados."""
        await self.session.commit()
        await self.session.refresh(probe)
        return probe
