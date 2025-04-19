from enum import StrEnum

from pydantic import BaseModel


class PlayerType(StrEnum):
    human = "human"
    random = "random"


class PlayerConfig(BaseModel):
    type: PlayerType
