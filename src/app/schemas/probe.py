from enum import Enum

from pydantic import BaseModel, Field


class DirectionEnum(str, Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"


class Probe(BaseModel):
    x: int = Field(..., description="Coordenada X da sonda")
    y: int = Field(..., description="Coordenada Y da sonda")
    direction: DirectionEnum = Field(
        ..., description="Direção inicial da sonda (NORTH, EAST, SOUTH, WEST)"
    )
