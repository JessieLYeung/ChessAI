"""
Rook chess piece implementation
"""

from .piece import Piece

class Rook(Piece):
    """Rook chess piece"""
    
    def get_valid_moves(self, board):
        """Get all valid moves for the rook"""
        moves = []
        
        # Horizontal and vertical directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for row_dir, col_dir in directions:
            for distance in range(1, 8):
                new_row = self.row + row_dir * distance
                new_col = self.col + col_dir * distance
                
                # Check if the new position is within the board
                if not (0 <= new_row <= 7 and 0 <= new_col <= 7):
                    break
                
                target_piece = board.get_piece(new_row, new_col)
                
                if target_piece is None:
                    # Empty square
                    moves.append((new_row, new_col))
                elif self.is_enemy(target_piece):
                    # Enemy piece - can capture
                    moves.append((new_row, new_col))
                    break
                else:
                    # Ally piece - cannot move here
                    break
        
        return moves
    
    def can_move_to(self, row, col, board):
        """Check if the rook can move to a specific position"""
        # Must be on the same row or column
        if self.row != row and self.col != col:
            return False
        
        # Check if path is clear
        row_dir = 0 if self.row == row else (1 if row > self.row else -1)
        col_dir = 0 if self.col == col else (1 if col > self.col else -1)
        
        current_row, current_col = self.row + row_dir, self.col + col_dir
        
        while current_row != row or current_col != col:
            if board.get_piece(current_row, current_col) is not None:
                return False
            current_row += row_dir
            current_col += col_dir
        
        # Check target square
        target_piece = board.get_piece(row, col)
        return target_piece is None or self.is_enemy(target_piece)