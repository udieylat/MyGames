import random

from cards.card import Card
from cards.compendium import Compendium
from constants import DEFAULT_NUM_CARDS_PER_PLAYER


class CardsRandomizer:
    @classmethod
    def draw_cards(
        cls,
        white_card_names: list[str] | None = None,
        black_card_names: list[str] | None = None,
        num_white_cards: int = DEFAULT_NUM_CARDS_PER_PLAYER,
        num_black_cards: int = DEFAULT_NUM_CARDS_PER_PLAYER,
        cards_pull: list[str] | None = None,
    ) -> tuple[list[Card], list[Card]]:
        if not cards_pull and cards_pull is not None:
            return [], []

        all_cards = Compendium.get_cards()
        if cards_pull is None:
            cards_pull = all_cards
        else:
            cards_pull = cls._get_cards(
                card_names=cards_pull,
                cards_pull=all_cards,
                total_num_cards=len(cards_pull),
            )
        if not white_card_names and not black_card_names:
            white_cards = cls._randomize_from_pull(
                cards_pull=cards_pull,
                num_cards=num_white_cards,
                ignore_cards=[],
            )
            black_cards = cls._randomize_from_pull(
                cards_pull=cards_pull,
                num_cards=num_black_cards,
                ignore_cards=white_cards,
            )
        elif white_card_names and not black_card_names:
            white_cards = cls._get_cards(
                card_names=white_card_names,
                cards_pull=cards_pull,
                total_num_cards=num_white_cards,
            )
            black_cards = cls._randomize_from_pull(
                cards_pull=cards_pull,
                num_cards=num_black_cards,
                ignore_cards=white_cards,
            )
        elif not white_card_names and black_card_names:
            black_cards = cls._get_cards(
                card_names=black_card_names,
                cards_pull=cards_pull,
                total_num_cards=num_black_cards,
            )
            white_cards = cls._randomize_from_pull(
                cards_pull=cards_pull,
                num_cards=num_white_cards,
                ignore_cards=black_cards,
            )
        else:
            white_cards = cls._get_cards(
                card_names=white_card_names,
                cards_pull=cards_pull,
                total_num_cards=num_white_cards,
            )
            black_cards = cls._get_cards(
                card_names=black_card_names,
                cards_pull=cards_pull,
                total_num_cards=num_black_cards,
                ignore_cards=white_cards,
            )
        return white_cards, black_cards

    @classmethod
    def _randomize_from_pull(
        cls,
        cards_pull: list[Card],
        num_cards: int,
        ignore_cards: list[Card],
    ) -> list[Card]:
        all_valid_cards = [
            card
            for card in cards_pull
            if card not in ignore_cards
        ]
        assert len(all_valid_cards) >= num_cards, "Cannot randomize enough cards"
        random.shuffle(all_valid_cards)
        return all_valid_cards[:num_cards]

    @classmethod
    def _get_cards(
        cls,
        card_names: list[str],
        cards_pull: list[Card],
        total_num_cards: int,
        ignore_cards: list[Card] = [],
    ) -> list[Card]:
        assert total_num_cards >= len(card_names), "Total num cards is larger than input card names list"
        name_to_card = {
            card.name: card
            for card in cards_pull
        }
        cards = [
            name_to_card[card_name]
            for card_name in card_names
        ]
        if total_num_cards == len(card_names):
            return cards

        cards += cls._randomize_from_pull(
            cards_pull=cards_pull,
            ignore_cards=cards + ignore_cards,
            num_cards=total_num_cards - len(cards),
        )
        assert total_num_cards == len(cards)
        return cards
