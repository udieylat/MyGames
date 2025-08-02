#!/usr/bin/env python3
"""
Flask backend API for the Magic Ball Game web interface.
Integrates with the existing Python game engine.
"""

import sys
import os
import json
import time
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from game_manager import GameManager
from game_config import GameConfig
from models import PlayerSign, GameStatus, TileType
from board_utils import BoardUtils
from cards.compendium import Compendium
from players.player_config import PlayerConfig, PlayerType, ScoreMultipliers

app = Flask(__name__)
CORS(app)  # Enable CORS for development

# Global game instance
game_manager = None
game_type = None  # 'human_vs_human' or 'human_vs_ai'
human_player_side = None  # 'white' or 'black'

@app.route('/')
def index():
    """Serve the main menu page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

def load_config_from_file(config_name):
    """Load game configuration from JSON file"""
    config_path = Path(__file__).parent.parent / 'config' / f'{config_name}.json'
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_name}.json not found")
    
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    # Create player configs
    white_config = PlayerConfig(
        type=PlayerType(config_data['white_player']['type']),
        score_multipliers=ScoreMultipliers(**config_data['white_player'].get('score_multipliers', {})) if 'score_multipliers' in config_data['white_player'] else None
    )
    
    black_config = PlayerConfig(
        type=PlayerType(config_data['black_player']['type']),
        score_multipliers=ScoreMultipliers(**config_data['black_player'].get('score_multipliers', {})) if 'score_multipliers' in config_data['black_player'] else None
    )
    
    return GameConfig(white_player=white_config, black_player=black_config)

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Start a new game"""
    global game_manager, game_type, human_player_side
    
    try:
        data = request.get_json() or {}
        game_type = data.get('game_type', 'human_vs_human')
        human_player_side = data.get('human_player_side', 'white')
        
        # Create game config based on game type
        if game_type == 'human_vs_human':
            config = GameConfig()  # Default human vs human
        elif game_type == 'human_vs_ai':
            if human_player_side == 'white':
                config = load_config_from_file('human_in_white_vs_ai')
            else:  # human_player_side == 'black'
                # Swap white and black configs
                base_config = load_config_from_file('human_in_white_vs_ai')
                config = GameConfig(
                    white_player=base_config.black_player,
                    black_player=base_config.white_player,
                    cards_config=base_config.cards_config
                )
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid game type'
            }), 400
        
        # Create new game manager
        game_manager = GameManager.new(config=config)
        
        print(f"Game manager created: {game_manager}")
        print(f"Game type: {game_type}")
        print(f"Human player side: {human_player_side}")
        print(f"Board: {game_manager._board._board}")
        print(f"Ball position: {game_manager._board.ball_position}")
        
        return jsonify({
            'success': True,
            'message': 'New game started',
            'game_state': get_game_state()
        })
    except Exception as e:
        print(f"Error creating new game: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_game_state():
    """Get current game state"""
    global game_manager
    
    if not game_manager:
        return {
            'success': False,
            'error': 'No active game'
        }
    
    try:
        # Get board state
        board = game_manager._board._board
        ball_position = game_manager._board.ball_position.value
        
        print(f"Board data: {board}")
        print(f"Ball position: {ball_position}")
        
        # Convert board to frontend format
        board_state = []
        for row in board:
            board_row = []
            for tile in row:
                # Convert TileType enum to string value
                tile_value = tile.value if hasattr(tile, 'value') else str(tile)
                if tile_value == 'W':
                    board_row.append('white')
                elif tile_value == 'B':
                    board_row.append('black')
                else:
                    board_row.append(None)
            board_state.append(board_row)
        
        print(f"Converted board state: {board_state}")
        
        # Get current player
        current_player = game_manager._player_turn.value
        
        # Get game status
        game_status = game_manager.game_status.value
        
        # Get player cards with more details
        white_cards = []
        for i, card in enumerate(game_manager._white_player.cards):
            if not card.already_used:
                white_cards.append({
                    'index': i,
                    'name': card.name,
                    'description': card.description(),
                })
        
        black_cards = []
        for i, card in enumerate(game_manager._black_player.cards):
            if not card.already_used:
                black_cards.append({
                    'index': i,
                    'name': card.name,
                    'description': card.description(),
                })
        
        return {
            'success': True,
            'board': board_state,
            'ball_position': ball_position,
            'current_player': current_player,
            'game_status': game_status,
            'white_cards': white_cards,
            'black_cards': black_cards,
            'white_cards_count': len(white_cards),
            'black_cards_count': len(black_cards),
            'game_type': game_type,
            'human_player_side': human_player_side
        }
    except Exception as e:
        print(f"Error getting game state: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/api/game/state', methods=['GET'])
def get_game_state_endpoint():
    """Get current game state"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        # Get board state
        board = game_manager._board._board
        ball_position = game_manager._board.ball_position.value
        
        # Convert board to frontend format
        board_state = []
        for row in board:
            board_row = []
            for tile in row:
                # Convert TileType enum to string value
                tile_value = tile.value if hasattr(tile, 'value') else str(tile)
                if tile_value == 'W':
                    board_row.append('white')
                elif tile_value == 'B':
                    board_row.append('black')
                else:
                    board_row.append(None)
            board_state.append(board_row)
        
        # Get current player
        current_player = game_manager._player_turn.value
        
        # Get game status
        game_status = game_manager.game_status.value
        
        # Get player cards with more details
        white_cards = []
        for i, card in enumerate(game_manager._white_player.cards):
            if not card.already_used:
                white_cards.append({
                    'index': i,
                    'name': card.name,
                    'description': 'description': card.description(),
                })
        
        black_cards = []
        for i, card in enumerate(game_manager._black_player.cards):
            if not card.already_used:
                black_cards.append({
                    'index': i,
                    'name': card.name,
                    'description': 'description': card.description(),
                })
        
        return jsonify({
            'success': True,
            'board': board_state,
            'ball_position': ball_position,
            'current_player': current_player,
            'game_status': game_status,
            'white_cards': white_cards,
            'black_cards': black_cards,
            'white_cards_count': len(white_cards),
            'black_cards_count': len(black_cards),
            'game_type': game_type,
            'human_player_side': human_player_side
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/game/move', methods=['POST'])
def make_move():
    """Make a move in the game"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        data = request.get_json()
        move_type = data.get('type')
        
        if move_type == 'push':
            target_tile = data.get('target_tile')
            game_manager.push(target_tile)
        elif move_type == 'card':
            card_index = data.get('card_index')
            move_index = data.get('move_index')
            game_manager.play_card(card_index, move_index)
        elif move_type == 'pass':
            game_manager.pass_turn()
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid move type'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Move made successfully',
            'game_state': get_game_state()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/game/ai-move', methods=['POST'])
def make_ai_move():
    """Make an AI move in the game"""
    global game_manager, game_type, human_player_side
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    if game_type != 'human_vs_ai':
        return jsonify({
            'success': False,
            'error': 'Not an AI game'
        }), 400
    
    try:
        # Check if it's AI's turn
        current_player = game_manager._player_turn.value
        ai_side = 'black' if human_player_side == 'white' else 'white'
        
        if current_player != ai_side:
            return jsonify({
                'success': False,
                'error': 'Not AI turn'
            }), 400
        
        # Get AI player
        ai_player = game_manager._black_player if ai_side == 'black' else game_manager._white_player
        
        # Get AI move
        ai_move = ai_player.get_move(game_manager._board, game_manager._player_turn)
        
        move_description = ''
        if ai_move is None:
            # AI passes turn
            game_manager.pass_turn()
            move_description = 'AI passes turn'
        else:
            # Execute AI move
            if hasattr(ai_move, 'card_index') and hasattr(ai_move, 'move_index'):
                # Card move
                card = ai_player.cards[ai_move.card_index]
                move_description = f'AI plays {card.name}'
                game_manager.play_card(ai_move.card_index, ai_move.move_index)
            else:
                # Push move
                move_description = f'AI pushes to {ai_move.target_tile}'
                game_manager.push(ai_move.target_tile)
        
        return jsonify({
            'success': True,
            'message': 'AI move made successfully',
            'move_description': move_description,
            'game_state': get_game_state()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/game/valid-moves', methods=['GET'])
def get_valid_moves():
    """Get valid moves for the current player"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        # Get current player
        current_player = game_manager._get_player()
        
        # Get available moves
        available_moves = []
        
        # Check for push moves
        for row in range(5):
            for col in range(5):
                tile = BoardUtils.coordinates_to_tile(row, col)
                try:
                    # Try to generate a push move
                    move = BoardUtils.generate_push_move(
                        player_sign=game_manager._player_turn,
                        target_tile=tile,
                        board=game_manager._board
                    )
                    available_moves.append({
                        'type': 'push',
                        'target_tile': tile,
                        'description': f'Push to {tile}'
                    })
                except:
                    pass
        
        # Check for card moves
        for i, card in enumerate(current_player.cards):
            if not card.already_used:
                card_moves = game_manager._get_available_card_moves(i)
                for j, move in enumerate(card_moves):
                    available_moves.append({
                        'type': 'card',
                        'card_index': i,
                        'move_index': j,
                        'description': f'{card.name}: {move.description}'
                    })
        
        return jsonify({
            'success': True,
            'valid_moves': available_moves
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/game/cards', methods=['GET'])
def get_player_cards():
    """Get current player's cards"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        current_player = game_manager._get_player()
        cards = []
        
        for i, card in enumerate(current_player.cards):
            if not card.already_used:
                cards.append({
                    'index': i,
                    'name': card.name,
                    'description': 'description': card.description(),
                })
        
        return jsonify({
            'success': True,
            'cards': cards
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/game/card-moves/<int:card_index>', methods=['GET'])
def get_card_moves(card_index):
    """Get available moves for a specific card"""
    global game_manager
    
    if not game_manager:
        return jsonify({
            'success': False,
            'error': 'No active game'
        }), 404
    
    try:
        current_player = game_manager._get_player()
        card = current_player.cards[card_index]
        
        if card.already_used:
            return jsonify({
                'success': False,
                'error': 'Card already used'
            }), 400
        
        card_moves = game_manager._get_available_card_moves(card_index)
        moves = []
        
        for i, move in enumerate(card_moves):
            moves.append({
                'index': i,
                'description': move.description,
                'card_name': card.name
            })
        
        return jsonify({
            'success': True,
            'card_name': card.name,
            'card_description': 'description': card.description(),
            'moves': moves
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Magic Ball Game API server...")
    print("Access the game at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
