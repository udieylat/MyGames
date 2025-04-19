import random

from cards.card import Card
from cards.charge import Charge
from cards.fire import Fire
from cards.jump import Jump
from cards.knife import Knife
from cards.pull import Pull
from cards.side_step import SideStep
from cards.spawn import Spawn
from cards.wall import Wall


class CardsRandomizer:
    @classmethod
    def draw_cards(
        cls,
        cards_pull: list[Card] | None = None,
    ) -> tuple[list[Card], list[Card]]:
        all_cards = (
            cls._full_compendium()
            if cards_pull is None
            else cards_pull[:]
        )
        random.shuffle(all_cards)
        return all_cards[:2], all_cards[2: 5]

    @classmethod
    def _full_compendium(cls) -> list[Card]:
        return [
            Wall(),
            Knife(),
            Charge(),
            # Diag(),
            Pull(),
            # Negate(),
            # Scare(),
            Fire(),
            SideStep(),
            Jump(),
            # Tank(),
            # Kamikaze(),
            Spawn(),
        ]
