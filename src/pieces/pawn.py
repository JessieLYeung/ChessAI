"""
Pawn chess piece implementation
"""

from .piece import Piece

class Pawn(Piece):
    """Pawn chess piece"""
    
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.en_passant_vulnerable = False
    
    def get_valid_moves(self, board):
        """Get all valid moves for the pawn"""
        moves = []
        direction = -1 if self.color == 'white' else 1
        
        # Forward moves
        new_row = self.row + direction
        if 0 <= new_row <= 7:
            # One square forward
            if board.get_piece(new_row, self.col) is None:
                moves.append((new_row, self.col))
                
                # Two squares forward (initial move)
                if not self.has_moved:
                    new_row2 = self.row + 2 * direction
                    if 0 <= new_row2 <= 7 and board.get_piece(new_row2, self.col) is None:
                        moves.append((new_row2, self.col))
        
        # Diagonal captures
        for col_offset in [-1, 1]:
            new_col = self.col + col_offset
            if 0 <= new_col <= 7 and 0 <= new_row <= 7:
                target_piece = board.get_piece(new_row, new_col)
                if target_piece and self.is_enemy(target_piece):
                    moves.append((new_row, new_col))
        
        # En passant captures
        if self.color == 'white' and self.row == 3:
            # Check left and right for enemy pawns that just moved two squares
            for col_offset in [-1, 1]:
                new_col = self.col + col_offset
                if 0 <= new_col <= 7:
                    adjacent_piece = board.get_piece(self.row, new_col)
                    if (isinstance(adjacent_piece, Pawn) and 
                        adjacent_piece.color == 'black' and 
                        getattr(adjacent_piece, 'en_passant_vulnerable', False)):
                        moves.append((self.row - 1, new_col))
        
        elif self.color == 'black' and self.row == 4:
            # Check left and right for enemy pawns that just moved two squares
            for col_offset in [-1, 1]:
                new_col = self.col + col_offset
                if 0 <= new_col <= 7:
                    adjacent_piece = board.get_piece(self.row, new_col)
                    if (isinstance(adjacent_piece, Pawn) and 
                        adjacent_piece.color == 'white' and 
                        getattr(adjacent_piece, 'en_passant_vulnerable', False)):
                        moves.append((self.row + 1, new_col))
        
        return moves
    
    def can_move_to(self, row, col, board):
        """Check if the pawn can move to a specific position"""
        return (row, col) in self.get_valid_moves(board)
    
    def move(self, row, col):
        """Move the pawn and handle special flags"""
        # Check if this is a two-square move for en passant
        if abs(row - self.row) == 2:
            self.en_passant_vulnerable = True
        else:
            self.en_passant_vulnerable = False
        
        super().move(row, col)
    
    def copy(self):
        """Create a copy of this pawn"""
        pawn_copy = Pawn(self.color, self.row, self.col)
        pawn_copy.has_moved = self.has_moved
        pawn_copy.en_passant_vulnerable = getattr(self, 'en_passant_vulnerable', False)
        return pawn_copy
    
    def is_promoting(self):
        """Check if the pawn is ready for promotion"""
        if self.color == 'white' and self.row == 0:
            return True
        elif self.color == 'black' and self.row == 7:
            return True
        return False