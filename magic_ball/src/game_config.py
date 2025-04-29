from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from players.player_config import PlayerConfig


class GameConfig(BaseModel):
    white_player: PlayerConfig = Field(default_factory=PlayerConfig.human)
    black_player: PlayerConfig = Field(default_factory=PlayerConfig.human)
    # TODO: move this to CardsConfig
    white_cards: list[str] | None = None
    black_cards: list[str] | None = None
    # TODO: add num_white_cards, num_black_cards and fix validator and cards randomization accordingly

    @model_validator(mode="after")
    def validate_cards(cls, config: GameConfig) -> GameConfig:
        white_cards = config.white_cards or []
        black_cards = config.black_cards or []

        if white_cards or black_cards:
            # Ensure all cards are lowercase
            if any(card != card.lower() for card in white_cards + black_cards):
                raise ValueError("All card names must be lowercase.")

            # Ensure no overlapping cards
            if set(white_cards) & set(black_cards):
                raise ValueError("white_cards and black_cards must not share any cards.")

        return config
