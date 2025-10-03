"""
AI Chess Bot - Main Entry Point
A fully functional chess game with player vs player and AI modes
Built with Python, Pygame, and the Minimax algorithm
"""

import pygame
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.game import ChessGame
from src.menu import MainMenu

def main():
    """Main entry point for the chess game"""
    pygame.init()
    
    # Initialize the main menu
    menu = MainMenu()
    game_mode = menu.run()
    
    if game_mode:
        # Start the chess game with selected mode
        game = ChessGame(game_mode)
        game.run()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()