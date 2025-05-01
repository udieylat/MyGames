from board import Board
from cards.card import Card
from helper import Helper
from models import PlayerSign
from move import Move
from players.player import Player, NoAvailableMoves
from players.player_config import PlayerConfig
from scores.scorer import Scorer


class BaseHeuristicPlayer(Player):
    """
    Basically a next-move scorer player.
    """
    def __init__(
        self,
        player_sign: PlayerSign,
        config: PlayerConfig,
    ):
        super().__init__(
            player_sign=player_sign,
        )
        self._scorer = Scorer(
            player_sign=player_sign,
            config=config,
        )

    def find_move(
        self,
        board: Board,
        player_cards: list[Card],
        opponent_cards: list[Card],
    ) -> Move:
        num_allowed_playable_cards = min(len(player_cards), len(opponent_cards))
        available_moves = Helper.get_available_moves(
            board=board,
            player_sign=self._player_sign,
            cards=self._cards,
            num_allowed_playable_cards=num_allowed_playable_cards,
        )
        if not available_moves:
            raise NoAvailableMoves()

        unused_player_cards = [
            card
            for card in player_cards
            if not card.already_used
        ]
        unused_opponent_cards = [
            card
            for card in opponent_cards
            if not card.already_used
        ]

        scores_and_moves = [
            (
                self._scorer.score_board(
                    board=move.result_board,
                    ball_position=move.result_ball_position,
                    num_unused_player_cards=len(unused_player_cards),
                    num_unused_opponent_cards=len(unused_opponent_cards),
                ),
                move,
            )
            for move in available_moves
        ]
        return max(
            scores_and_moves,
            key=lambda scores_and_move: scores_and_move[0],
        )[1]
