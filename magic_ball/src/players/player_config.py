from enum import StrEnum

from pydantic import BaseModel


class PlayerType(StrEnum):
    human = "human"
    random = "random"
    base_heuristic = "base_heuristic"


class PlayerConfig(BaseModel):
    type: PlayerType
