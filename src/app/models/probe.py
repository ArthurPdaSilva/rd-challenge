from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.schemas.probe import ProbeBase

if TYPE_CHECKING:
    from app.models.grid import Grid


class Probe(ProbeBase, table=True):
    __tablename__ = "probes"

    id: Optional[int] = Field(primary_key=True)
    grid: Optional["Grid"] = Relationship(
        back_populates="probe", sa_relationship_kwargs={"uselist": False}
    )
