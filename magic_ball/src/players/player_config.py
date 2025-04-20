from enum import StrEnum

from pydantic import BaseModel


class PlayerType(StrEnum):
    human = "human"
    random = "random"
    base_heuristic = "base_heuristic"


class ScoreMultipliers(BaseModel):
    pass


class PlayerConfig(BaseModel):
    type: PlayerType
    score_multipliers: ScoreMultipliers | None = None
