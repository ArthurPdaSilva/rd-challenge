from enum import Enum

from pydantic import Field
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


class ProbeLaunch(ProbeBase):
    pass


class ProbeResponse(ProbeBase):
    id: int = Field(..., description="ID da sonda lançada")


class ProbeMove(SQLModel):
    id: int = Field(..., description="ID da sonda a ser movida")
    command: str = Field(
        ..., description="Sequência de comandos para movimentar a sonda Exp: (MRM)"
    )


class ProbesPositionsResponse(SQLModel):
    probes: list[ProbeResponse] = Field(
        ..., description="Lista de sondas e suas posições atuais"
    )
