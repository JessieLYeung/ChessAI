"""
Knight chess piece implementation
"""

from .piece import Piece

class Knight(Piece):
    """Knight chess piece"""
    
    def get_valid_moves(self, board):
        """Get all valid moves for the knight"""
        moves = []
        
        # Knight moves in L-shape: 2 squares in one direction, 1 in perpendicular
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for row_offset, col_offset in knight_moves:
            new_row = self.row + row_offset
            new_col = self.col + col_offset
            
            # Check if the new position is within the board
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                target_piece = board.get_piece(new_row, new_col)
                
                # Can move to empty square or capture enemy piece
                if target_piece is None or self.is_enemy(target_piece):
                    moves.append((new_row, new_col))
        
        return moves
    
    def can_move_to(self, row, col, board):
        """Check if the knight can move to a specific position"""
        row_diff = abs(row - self.row)
        col_diff = abs(col - self.col)
        
        # Knight moves in L-shape
        if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
            return False
        
        # Check target square
        target_piece = board.get_piece(row, col)
        return target_piece is None or self.is_enemy(target_piece)