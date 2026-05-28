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
