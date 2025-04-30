import json
import time

from cards.compendium import Compendium
from game_simulator import GameSimulator

sim = GameSimulator.from_config_filename("config/ai_vs_ai.json")
card_to_summary = {}

for card_name in Compendium.get_cards_names():
	config = sim.clone_config()
	config.white_cards = [card_name]
	s = GameSimulator(config)
	print(f"{time.strftime('%c')}: {card_name}")
	card_to_summary[card_name] = s.run(10000)

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

open("results/sim.json", 'w').write(json.dumps(results, indent=2))
