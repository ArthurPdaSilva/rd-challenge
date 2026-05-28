from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.probe import Probe


class Grid(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dimension_x: int = Field(..., description="O número de colunas na grade")
    dimension_y: int = Field(..., description="O número de linhas na grade")
    probe_id: int = Field(foreign_key="probes.id", unique=True)
    probe: "Probe" = Relationship(back_populates="grid")
