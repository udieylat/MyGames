from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from cards.cards_config import CardsConfig
from players.player_config import PlayerConfig


class GameConfig(BaseModel):
    white_player: PlayerConfig = Field(default_factory=PlayerConfig.human)
    black_player: PlayerConfig = Field(default_factory=PlayerConfig.human)
    cards_config: CardsConfig = Field(default_factory=CardsConfig)

    @model_validator(mode="after")
    def validate_cards(cls, config: GameConfig) -> GameConfig:
        white_cards_names = config.cards_config.white_cards_names or []
        black_cards_names = config.cards_config.black_cards_names or []

        if white_cards_names or black_cards_names:
            # Ensure all cards are lowercase
            if any(card != card.lower() for card in white_cards_names + black_cards_names):
                raise ValueError("All card names must be lowercase.")

            # Ensure no overlapping cards
            if set(white_cards_names) & set(black_cards_names):
                raise ValueError("white_cards_names and black_cards_names must not share any cards.")

        return config

    def clone_with_white_cards(
        self,
        white_cards_names: list[str],
    ) -> GameConfig:
        clone = self.model_copy()
        clone.cards_config = self.cards_config.model_copy()
        clone.cards_config.white_cards_name = white_cards_names
        return clone

    def clone_with_black_cards(
        self,
        black_cards_names: list[str],
    ) -> GameConfig:
        clone = self.model_copy()
        clone.cards_config = self.cards_config.model_copy()
        clone.cards_config.black_cards_names = black_cards_names
        return clone
