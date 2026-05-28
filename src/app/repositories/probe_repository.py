from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.probe import Probe


class ProbeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, probe: Probe):
        self.session.add(probe)
        await self.session.commit()
        await self.session.refresh(probe)
        return probe

    async def get_by_id(self, probe_id: int):
        result = await self.session.get(Probe, probe_id)
        return result

    async def update(self, probe: Probe):
        await self.session.commit()
        await self.session.refresh(probe)
        return probe
