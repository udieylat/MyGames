import unittest

from cards.cards_randomizer import CardsRandomizer
from constants import DEFAULT_NUM_CARDS_PER_PLAYER


class TestCardsRandomizer(unittest.TestCase):
    def test_draw_cards_from_partial_white_cards(self):
        card_name = "knife"
        white_cards, black_cards = CardsRandomizer.draw_cards(
            white_card_names=[
                card_name,
            ],
        )
        self.assertEqual(DEFAULT_NUM_CARDS_PER_PLAYER, len(white_cards))
        self.assertEqual(DEFAULT_NUM_CARDS_PER_PLAYER, len(black_cards))
        self.assertIn(card_name, [card.name for card in white_cards])
        self.assertNotIn(card_name, [card.name for card in black_cards])

    def test_draw_cards_from_partial_black_cards(self):
        card_name = "wall"
        white_cards, black_cards = CardsRandomizer.draw_cards(
            black_card_names=[
                card_name,
            ],
        )
        self.assertEqual(DEFAULT_NUM_CARDS_PER_PLAYER, len(white_cards))
        self.assertEqual(DEFAULT_NUM_CARDS_PER_PLAYER, len(black_cards))
        self.assertNotIn(card_name, [card.name for card in white_cards])
        self.assertIn(card_name, [card.name for card in black_cards])

    def test_draw_cards_num_cards(self):
        white_cards, black_cards = CardsRandomizer.draw_cards(
            num_white_cards=4,
            num_black_cards=5,
        )
        self.assertEqual(4, len(white_cards))
        self.assertEqual(5, len(black_cards))
        common_card_names = {card.name for card in white_cards} & {card.name for card in black_cards}
        self.assertSetEqual(set(), common_card_names)
