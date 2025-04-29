import random

from cards.bishop import Bishop
from cards.card import Card
from cards.charge import Charge
from cards.dagger import Dagger
from cards.fire import Fire
from cards.jump import Jump
from cards.kamikaze import Kamikaze
from cards.knife import Knife
from cards.peace import Peace
# from cards.pull import Pull
from cards.scare import Scare
from cards.side_step import SideStep
from cards.spawn import Spawn
from cards.tank import Tank
from cards.wall import Wall


class CardsRandomizer:
    @classmethod
    def draw_cards(
        cls,
        # TODO: receive CardsConfig with num white/black cards to randomize
        white_card_names: list[str] | None = None,
        black_card_names: list[str] | None = None,
        cards_pull: list[Card] | None = None,
    ) -> tuple[list[Card], list[Card]]:
        if not cards_pull and cards_pull is not None:
            return [], []

        cards_pull = (
            cls._full_compendium()
            if cards_pull is None
            else cards_pull[:]
        )
        if not white_card_names and not black_card_names:
            white_cards = cls._randomize_from_pull(
                cards_pull=cards_pull,
                ignore_card_names=[],
            )
            black_cards = cls._randomize_from_pull(
                cards_pull=cards_pull,
                ignore_card_names=white_card_names,
            )
        elif white_card_names and not black_card_names:
            white_cards = cls._get_cards(
                card_names=white_card_names,
                cards_pull=cards_pull,
            )
            black_cards = cls._randomize_from_pull(
                cards_pull=cards_pull,
                ignore_card_names=white_card_names,
            )
        elif not white_card_names and black_card_names:
            black_cards = cls._get_cards(
                card_names=black_card_names,
                cards_pull=cards_pull,
            )
            white_cards = cls._randomize_from_pull(
                cards_pull=cards_pull,
                ignore_card_names=black_card_names,
            )
        else:
            white_cards = cls._get_cards(
                card_names=white_card_names,
                cards_pull=cards_pull,
            )
            black_cards = cls._get_cards(
                card_names=black_card_names,
                cards_pull=cards_pull,
            )
        return white_cards, black_cards

    @classmethod
    def _randomize_from_pull(
        cls,
        cards_pull: list[Card],
        ignore_card_names: list[str],
        num_cards: int = 3,
    ) -> list[Card]:
        all_valid_cards = [
            card
            for card in cards_pull
            if card.name not in ignore_card_names
        ]
        assert len(all_valid_cards) >= num_cards, "Cannot randomize enough cards"
        random.shuffle(all_valid_cards)
        return all_valid_cards[:num_cards]

    @classmethod
    def _get_cards(
        cls,
        card_names: list[str],
        cards_pull: list[Card],
    ) -> list[Card]:
        name_to_card = {
            card.name: card
            for card in cards_pull
        }
        return [
            name_to_card[card_name]
            for card_name in card_names
        ]

    @classmethod
    def _full_compendium(cls) -> list[Card]:
        return [
            Wall(),
            Knife(),
            Charge(),
            Bishop(),
            # Pull(),
            # Negate(),
            Scare(),
            Fire(),
            SideStep(),
            Jump(),
            Tank(),
            Kamikaze(),
            Spawn(),
            Dagger(),
            Peace(),
        ]
