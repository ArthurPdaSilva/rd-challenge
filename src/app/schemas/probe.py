from enum import Enum

from pydantic import BaseModel, Field
from sqlmodel import SQLModel


class DirectionEnum(str, Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class ProbeBase(SQLModel):
    x: int = Field(..., description="Coordenada X da sonda")
    y: int = Field(..., description="Coordenada Y da sonda")
    direction: DirectionEnum = Field(
        ..., description="Direção inicial da sonda (NORTH, EAST, SOUTH, WEST)"
    )


class ProbeCreate(ProbeBase):
    pass
