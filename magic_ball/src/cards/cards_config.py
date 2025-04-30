from pydantic import BaseModel

from cards.card import Card
from constants import DEFAULT_NUM_CARDS_PER_PLAYER


class CardsConfig(BaseModel):
    white_card_names: list[str] | None = None
    black_card_names: list[str] | None = None
    num_white_cards: int = DEFAULT_NUM_CARDS_PER_PLAYER
    num_black_cards: int = DEFAULT_NUM_CARDS_PER_PLAYER
    cards_pull: list[str] | None = None
