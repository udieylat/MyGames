from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class PlayerType(StrEnum):
    human = "human"
    random = "random"
    base_heuristic = "base_heuristic"


class ScoreMultipliers(BaseModel):
    score_per_pawn: int
    score_per_free_pawn: int
    free_pawn_score_per_distance_from_start_tile: int
    penalty_score_per_used_card: int
    ball_position_score: int
    no_cards_play_available_penalty_score: int


class PlayerConfig(BaseModel):
    type: PlayerType
    score_multipliers: ScoreMultipliers | None = None
    random_tie_break: bool = True

    @classmethod
    def human(cls) -> PlayerConfig:
        return PlayerConfig(
            type=PlayerType.human,
        )

    @classmethod
    def default_ai_opponent(cls, random_tie_break: bool = True) -> PlayerConfig:
        return PlayerConfig(
            type=PlayerType.base_heuristic,
            score_multipliers=ScoreMultipliers(
                score_per_pawn=10,
                score_per_free_pawn=100,
                free_pawn_score_per_distance_from_start_tile=400,
                penalty_score_per_used_card=-150,
                ball_position_score=100,
                no_cards_play_available_penalty_score=-100,
            ),
            random_tie_break=random_tie_break,
        )
