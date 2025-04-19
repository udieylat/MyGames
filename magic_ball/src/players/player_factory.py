# from models import PlayerSign
# from players.human_player import HumanPlayer
# from players.player import Player
#
#
# class PlayerFactory:
#     def generate_player(
#         self,
#         player_type: PlayerType,
#         player_sign: PlayerSign,
#     ) -> Player:
#         match player_type:
#             case PlayerType.human:
#                 return HumanPlayer(
#                     player_sign=player_sign,
#                 )
#             case PlayerType.ai:
#                 # TODO
#                 raise NotImplemented
