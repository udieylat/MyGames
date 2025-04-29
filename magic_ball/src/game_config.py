from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from players.player_config import PlayerConfig


class GameConfig(BaseModel):
    white_player: PlayerConfig = Field(default_factory=PlayerConfig.human)
    black_player: PlayerConfig = Field(default_factory=PlayerConfig.human)
    white_cards: list[str] | None = None
    black_cards: list[str] | None = None

    @model_validator(mode="after")
    def validate_cards(cls, config: GameConfig) -> GameConfig:
        white_cards = config.white_cards
        black_cards = config.black_cards

        if white_cards is not None and black_cards is not None:
            # Ensure both lists have exactly 3 items
            if len(white_cards) != 3 or len(black_cards) != 3:
                raise ValueError("Each of white_cards and black_cards must contain exactly 3 cards.")

            # Ensure all cards are lowercase
            if any(card != card.lower() for card in white_cards + black_cards):
                raise ValueError("All card names must be lowercase.")

            # Ensure no overlapping cards
            if set(white_cards) & set(black_cards):
                raise ValueError("white_cards and black_cards must not share any cards.")

        return config
