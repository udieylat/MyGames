import argparse
import itertools
import json
import time

from game_config import GameConfig
from game_simulator import GameSimulator

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output_filename", default="results/new_sim.json")
parser.add_argument("-n", "--num_games", type=int, default=10000)
args = parser.parse_args()

base_config = GameConfig.model_validate(json.load(open("config/ai_vs_ai.json")))

# penalty_score_per_used_card, ball_position_score, no_cards_play_available_penalty_score
configs = [
    ("current", -150, 100, -100),  # Current strategy (relatively cards averse)
    ("aggressive", -50, 0, 0),  # Cards inclined, more aggressive
    ("defensive", -250, 100, -1000), # Very cards averse, especially last playable card
]

name_to_summary = {}
for config_1, config_2 in itertools.product(configs, configs):
    name_1, penalty_score_per_used_card_1, ball_position_score_1, no_cards_play_available_penalty_score_1 = config_1
    name_2, penalty_score_per_used_card_2, ball_position_score_2, no_cards_play_available_penalty_score_2 = config_2
    config = base_config.model_copy()
    config.white_player.score_multipliers.penalty_score_per_used_card = penalty_score_per_used_card_1
    config.white_player.score_multipliers.ball_position_score = ball_position_score_1
    config.white_player.score_multipliers.no_cards_play_available_penalty_score = no_cards_play_available_penalty_score_1
    config.black_player.score_multipliers.penalty_score_per_used_card = penalty_score_per_used_card_2
    config.black_player.score_multipliers.ball_position_score = ball_position_score_2
    config.black_player.score_multipliers.no_cards_play_available_penalty_score = no_cards_play_available_penalty_score_2

    simulator = GameSimulator(
        config=config,
    )
    print(f"{time.strftime('%c')}: {name_1} v {name_2}")
    summary = simulator.run(
        num_games=args.num_games,
    )
    print(f"W: {summary.num_white_wins}, D: {summary.num_draws}, B: {summary.num_black_wins}")
    name_to_summary[f"{name_1}_v_{name_2}"] = summary

runtime_sec = sum(summary.runtime_sec for summary in name_to_summary.values())
print(f"Full simulation runtime: {runtime_sec:.2f}")

results = {
    name: (
        summary.num_white_wins,
        summary.num_draws,
        summary.num_black_wins,
    )
    for name, summary in name_to_summary.items()
}

open(args.output_filename, 'w').write(json.dumps(results, indent=2))
