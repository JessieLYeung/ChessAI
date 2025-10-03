"""
Chess pieces module - imports all piece classes
"""

from .piece import Piece
from .pawn import Pawn
from .rook import Rook
from .knight import Knight
from .bishop import Bishop
from .queen import Queen
from .king import King

__all__ = ['Piece', 'Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King']