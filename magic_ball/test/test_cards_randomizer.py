import unittest

from cards.cards_randomizer import CardsRandomizer


class TestCardsRandomizer(unittest.TestCase):
    def test_draw_cards_from_partial_white_cards(self):
        card_name = "knife"
        white_cards, black_cards = CardsRandomizer.draw_cards(
            white_card_names=[
                card_name,
            ],
        )
        self.assertEqual(3, len(white_cards))
        self.assertEqual(3, len(black_cards))
        self.assertIn(card_name, [card.name for card in white_cards])
        self.assertNotIn(card_name, [card.name for card in black_cards])

    def test_draw_cards_from_partial_black_cards(self):
        card_name = "wall"
        white_cards, black_cards = CardsRandomizer.draw_cards(
            black_card_names=[
                card_name,
            ],
        )
        self.assertEqual(3, len(white_cards))
        self.assertEqual(3, len(black_cards))
        self.assertNotIn(card_name, [card.name for card in white_cards])
        self.assertIn(card_name, [card.name for card in black_cards])
