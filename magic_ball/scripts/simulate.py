import argparse
import json
import time

from cards.compendium import Compendium
from game_config import GameConfig
from game_simulator import GameSimulator

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_filename", default="config/ai_vs_ai.json")
parser.add_argument("-o", "--output_filename", default="results/new_sim.json")
parser.add_argument("-n", "--num_games", type=int, default=10000)
parser.add_argument("-p", "--player", choices=["white", "black"], default="white")
args = parser.parse_args()

base_config = GameConfig.model_validate(json.load(open(args.input_filename)))
card_to_summary = {}

for card_name in Compendium.get_cards_names():
    config = base_config.model_copy()
    if args.player == "white":
        config.cards_config.white_card_names = [
            card_name,
        ]
    else:
        assert args.player == "black"
        config.cards_config.black_card_names = [
            card_name,
        ]
    simulator = GameSimulator(
        config=config,
    )
    print(f"{time.strftime('%c')}: {card_name}")
    summary = simulator.run(
        num_games=args.num_games,
    )
    print(f"W: {summary.num_white_wins}, D: {summary.num_draws}, B: {summary.num_black_wins}")
    card_to_summary[card_name] = summary

runtime_sec = sum(summary.runtime_sec for summary in card_to_summary.values())
print(f"Full simulation runtime: {runtime_sec:.2f}")

results = {
    card_name: (
        summary.num_white_wins,
        summary.num_draws,
        summary.num_black_wins,
    )
    for card_name, summary in card_to_summary.items()
}

open(args.output_filename, 'w').write(json.dumps(results, indent=2))
