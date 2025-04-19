import random

from cards.card import Card


class CardsRandomizer:
    @classmethod
    def draw_cards(cls) -> tuple[list[Card], list[Card]]:
        all_cards = [
            # TODO
        ]
        random.shuffle(all_cards)
        return all_cards[:2], all_cards[2: 5]
