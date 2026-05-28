from typing import Optional

from sqlmodel import Field

from app.schemas.probe import ProbeBase


class Probe(ProbeBase, table=True):
    __tablename__ = "probes"

    id: Optional[int] = Field(default=None, primary_key=True)
