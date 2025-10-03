"""
Game statistics and utilities
"""

import json
import os
from datetime import datetime

class GameStats:
    """Track and manage game statistics"""
    
    def __init__(self):
        self.stats_file = "game_stats.json"
        self.stats = self._load_stats()
    
    def _load_stats(self):
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'total_games': 0,
            'pvp_games': 0,
            'ai_games': 0,
            'player_wins': {'white': 0, 'black': 0},
            'ai_wins': 0,
            'draws': 0,
            'average_game_length': 0,
            'last_played': None
        }
    
    def _save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def record_game(self, game_mode, winner, move_count):
        """Record a completed game"""
        self.stats['total_games'] += 1
        self.stats['last_played'] = datetime.now().isoformat()
        
        if game_mode == 'pvp':
            self.stats['pvp_games'] += 1
            if winner:
                self.stats['player_wins'][winner] += 1
            else:
                self.stats['draws'] += 1
        
        elif game_mode == 'ai':
            self.stats['ai_games'] += 1
            if winner == 'white':  # Assuming player is usually white
                self.stats['player_wins']['white'] += 1
            elif winner == 'black':
                self.stats['ai_wins'] += 1
            else:
                self.stats['draws'] += 1
        
        # Update average game length
        current_avg = self.stats['average_game_length']
        total_games = self.stats['total_games']
        self.stats['average_game_length'] = ((current_avg * (total_games - 1)) + move_count) / total_games
        
        self._save_stats()
    
    def get_stats_summary(self):
        """Get a formatted summary of statistics"""
        if self.stats['total_games'] == 0:
            return ["No games played yet!"]
        
        summary = [
            f"Total Games: {self.stats['total_games']}",
            f"PvP Games: {self.stats['pvp_games']}",
            f"AI Games: {self.stats['ai_games']}",
            f"White Wins: {self.stats['player_wins']['white']}",
            f"Black Wins: {self.stats['player_wins']['black']}",
            f"AI Wins: {self.stats['ai_wins']}",
            f"Draws: {self.stats['draws']}",
            f"Avg Game Length: {self.stats['average_game_length']:.1f} moves"
        ]
        
        if self.stats['last_played']:
            try:
                last_date = datetime.fromisoformat(self.stats['last_played'])
                summary.append(f"Last Played: {last_date.strftime('%Y-%m-%d %H:%M')}")
            except:
                pass
        
        return summary

class MoveNotationConverter:
    """Convert moves to and from algebraic notation"""
    
    @staticmethod
    def position_to_notation(row, col):
        """Convert board position to algebraic notation"""
        return f"{chr(ord('a') + col)}{8 - row}"
    
    @staticmethod
    def notation_to_position(notation):
        """Convert algebraic notation to board position"""
        if len(notation) != 2:
            return None
        
        col = ord(notation[0].lower()) - ord('a')
        row = 8 - int(notation[1])
        
        if 0 <= row <= 7 and 0 <= col <= 7:
            return (row, col)
        return None
    
    @staticmethod
    def move_to_notation(from_pos, to_pos, piece_name, captured=False, check=False, checkmate=False):
        """Convert move to algebraic notation"""
        from_notation = MoveNotationConverter.position_to_notation(from_pos[0], from_pos[1])
        to_notation = MoveNotationConverter.position_to_notation(to_pos[0], to_pos[1])
        
        # Basic notation
        if piece_name.lower() == 'pawn':
            if captured:
                notation = f"{from_notation[0]}x{to_notation}"
            else:
                notation = to_notation
        else:
            piece_symbol = piece_name[0].upper()
            if captured:
                notation = f"{piece_symbol}x{to_notation}"
            else:
                notation = f"{piece_symbol}{to_notation}"
        
        # Add check/checkmate indicators
        if checkmate:
            notation += "#"
        elif check:
            notation += "+"
        
        return notation

class GameSaver:
    """Save and load game states"""
    
    @staticmethod
    def save_game(board, filename=None):
        """Save current game state"""
        if filename is None:
            filename = f"saved_game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        game_data = {
            'board_state': board.get_board_state(),
            'current_player': board.current_player,
            'move_history': board.move_history,
            'game_over': board.game_over,
            'winner': board.winner,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(game_data, f, indent=2)
            return True
        except:
            return False
    
    @staticmethod
    def load_game(filename):
        """Load a saved game state"""
        try:
            with open(filename, 'r') as f:
                game_data = json.load(f)
            return game_data
        except:
            return None
    
    @staticmethod
    def get_saved_games():
        """Get list of saved game files"""
        saved_games = []
        for filename in os.listdir('.'):
            if filename.startswith('saved_game_') and filename.endswith('.json'):
                try:
                    with open(filename, 'r') as f:
                        data = json.load(f)
                    timestamp = data.get('timestamp', 'Unknown')
                    saved_games.append((filename, timestamp))
                except:
                    pass
        
        return sorted(saved_games, key=lambda x: x[1], reverse=True)