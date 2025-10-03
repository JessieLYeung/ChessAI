"""
King chess piece implementation
"""

from .piece import Piece

class King(Piece):
    """King chess piece"""
    
    def get_valid_moves(self, board):
        """Get all valid moves for the king"""
        moves = []
        
        # King moves one square in any direction
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for row_dir, col_dir in directions:
            new_row = self.row + row_dir
            new_col = self.col + col_dir
            
            # Check if the new position is within the board
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                target_piece = board.get_piece(new_row, new_col)
                
                # Can move to empty square or capture enemy piece
                if target_piece is None or self.is_enemy(target_piece):
                    # Check if the move would put the king in check
                    if not board.would_be_in_check(self.color, self.row, self.col, new_row, new_col):
                        moves.append((new_row, new_col))
        
        # Castling moves
        castling_moves = self._get_castling_moves(board)
        moves.extend(castling_moves)
        
        return moves
    
    def can_move_to(self, row, col, board):
        """Check if the king can move to a specific position"""
        row_diff = abs(row - self.row)
        col_diff = abs(col - self.col)
        
        # Regular king move (one square in any direction)
        if row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff > 0):
            target_piece = board.get_piece(row, col)
            if target_piece is None or self.is_enemy(target_piece):
                # Check if move would put king in check
                return not board.would_be_in_check(self.color, self.row, self.col, row, col)
        
        # Castling move (special case)
        if row == self.row and abs(col - self.col) == 2:
            return self._can_castle(row, col, board)
        
        return False
    
    def _get_castling_moves(self, board):
        """Get available castling moves"""
        if self.has_moved or board.is_in_check(self.color):
            return []
        
        moves = []
        row = self.row
        
        # Kingside castling
        if self._can_castle(row, self.col + 2, board):
            moves.append((row, self.col + 2))
        
        # Queenside castling
        if self._can_castle(row, self.col - 2, board):
            moves.append((row, self.col - 2))
        
        return moves
    
    def _can_castle(self, target_row, target_col, board):
        """Check if castling is possible to the target position"""
        if self.has_moved or board.is_in_check(self.color):
            return False
        
        if target_row != self.row:
            return False
        
        # Determine castling direction
        if target_col == self.col + 2:  # Kingside
            rook_col = 7
            squares_to_check = [self.col + 1, self.col + 2]
            squares_between = [self.col + 1]
        elif target_col == self.col - 2:  # Queenside
            rook_col = 0
            squares_to_check = [self.col - 1, self.col - 2]
            squares_between = [self.col - 1, self.col - 2, self.col - 3]
        else:
            return False
        
        # Check if rook exists and hasn't moved
        rook = board.get_piece(self.row, rook_col)
        if not rook or rook.__class__.__name__ != 'Rook' or rook.has_moved:
            return False
        
        # Check if squares between king and rook are empty
        for col in squares_between:
            if board.get_piece(self.row, col) is not None:
                return False
        
        # Check if king would pass through or end up in check
        for col in squares_to_check:
            if board.would_be_in_check(self.color, self.row, self.col, self.row, col):
                return False
        
        return True