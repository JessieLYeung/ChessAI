"""
Base class for all chess pieces
"""

from abc import ABC, abstractmethod
import pygame
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from src.constants import SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y
except ImportError:
    from constants import SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y

class Piece(ABC):
    """Abstract base class for all chess pieces"""
    
    def __init__(self, color, row, col):
        """
        Initialize a chess piece
        
        Args:
            color (str): 'white' or 'black'
            row (int): Row position on the board (0-7)
            col (int): Column position on the board (0-7)
        """
        self.color = color
        self.row = row
        self.col = col
        self.has_moved = False
        self.image = None
        
    @abstractmethod
    def get_valid_moves(self, board):
        """
        Get all valid moves for this piece
        
        Args:
            board: The chess board object
            
        Returns:
            list: List of tuples (row, col) representing valid moves
        """
        pass
    
    @abstractmethod
    def can_move_to(self, row, col, board):
        """
        Check if the piece can move to a specific position
        
        Args:
            row (int): Target row
            col (int): Target column
            board: The chess board object
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        pass
    
    def move(self, row, col):
        """
        Move the piece to a new position
        
        Args:
            row (int): New row position
            col (int): New column position
        """
        self.row = row
        self.col = col
        self.has_moved = True
    
    def copy(self):
        """
        Create a copy of this piece
        
        Returns:
            Piece: A new instance of the same piece type
        """
        piece_copy = self.__class__(self.color, self.row, self.col)
        piece_copy.has_moved = self.has_moved
        return piece_copy
    
    def is_enemy(self, other_piece):
        """
        Check if another piece is an enemy
        
        Args:
            other_piece: Another chess piece
            
        Returns:
            bool: True if the other piece is an enemy
        """
        return other_piece is not None and other_piece.color != self.color
    
    def is_ally(self, other_piece):
        """
        Check if another piece is an ally
        
        Args:
            other_piece: Another chess piece
            
        Returns:
            bool: True if the other piece is an ally
        """
        return other_piece is not None and other_piece.color == self.color
    
    def get_piece_symbol(self):
        """
        Get a text representation of the piece
        
        Returns:
            str: Single character representing the piece
        """
        symbol_map = {
            'pawn': 'P',
            'rook': 'R',
            'knight': 'N',
            'bishop': 'B',
            'queen': 'Q',
            'king': 'K'
        }
        symbol = symbol_map.get(self.__class__.__name__.lower(), '?')
        return symbol.lower() if self.color == 'black' else symbol
    
    def draw(self, screen):
        """
        Draw the piece on the screen
        
        Args:
            screen: Pygame screen surface
        """
        if self.image:
            x = BOARD_OFFSET_X + self.col * SQUARE_SIZE
            y = BOARD_OFFSET_Y + self.row * SQUARE_SIZE
            screen.blit(self.image, (x, y))
        else:
            # Draw a simple text representation if no image is available
            font = pygame.font.Font(None, 36)
            text = font.render(self.get_piece_symbol(), True, (0, 0, 0))
            x = BOARD_OFFSET_X + self.col * SQUARE_SIZE + SQUARE_SIZE // 4
            y = BOARD_OFFSET_Y + self.row * SQUARE_SIZE + SQUARE_SIZE // 4
            screen.blit(text, (x, y))
    
    def load_image(self, image_path):
        """
        Load the piece image from file
        
        Args:
            image_path (str): Path to the image file
        """
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        except pygame.error:
            print(f"Could not load image: {image_path}")
            self.image = None
    
    def __str__(self):
        """String representation of the piece"""
        return f"{self.color} {self.__class__.__name__} at ({self.row}, {self.col})"
    
    def __repr__(self):
        """Official string representation of the piece"""
        return self.__str__()