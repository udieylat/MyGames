from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class PlayerType(StrEnum):
    human = "human"
    random = "random"
    base_heuristic = "base_heuristic"


class ScoreMultipliers(BaseModel):
    num_unused_player_cards_score: int
    ball_position_score: int


class PlayerConfig(BaseModel):
    type: PlayerType
    score_multipliers: ScoreMultipliers | None = None

    @classmethod
    def human(cls) -> PlayerConfig:
        return PlayerConfig(
            type=PlayerType.human,
        )
