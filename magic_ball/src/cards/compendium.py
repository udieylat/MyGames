import math

from cards.bishop import Bishop
from cards.card import Card
from cards.charge import Charge
from cards.dagger import Dagger
from cards.fire import Fire
from cards.forklift import Forklift
from cards.jump import Jump
from cards.kamikaze import Kamikaze
from cards.knife import Knife
from cards.knight import Knight
from cards.peace import Peace
from cards.catapult import Catapult
from cards.side_step import SideStep
from cards.spawn import Spawn
from cards.tank import Tank
from cards.wall import Wall
from constants import DEFAULT_NUM_CARDS_PER_PLAYER


class Compendium:
    @classmethod
    def get_cards(cls) -> list[Card]:
        return [
            Wall(),
            Knife(),
            Charge(),
            Bishop(),
            Catapult(),
            Fire(),
            SideStep(),
            Jump(),
            Tank(),
            Kamikaze(),
            Spawn(),
            Dagger(),
            Peace(),
            Knight(),
            Forklift(),
        ]

    @classmethod
    def get_cards_names(cls) -> list[str]:
        return [
            card.name
            for card in cls.get_cards()
        ]

    @classmethod
    def get_num_decks_options(
        cls,
        num_cards: int = DEFAULT_NUM_CARDS_PER_PLAYER,
        num_cards_in_pull: int | None = None,
    ) -> int:
        if num_cards_in_pull is None:
            num_cards_in_pull = len(cls.get_cards())
        return math.comb(num_cards_in_pull, num_cards)
