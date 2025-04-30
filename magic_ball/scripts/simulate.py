from cards.compendium import Compendium
from game_simulator import GameSimulator

sim = GameSimulator.from_config_filename("config/ai_vs_ai.json")
card_to_summary = {}

for card_name in Compendium.get_cards_names():
	config = sim.clone_config()
	config.white_cards = [card_name]
	s = GameSimulator(config)
	print(card_name)
	card_to_summary[card_name] = s.run(10000)

