"""
Chess board representation and game state management
"""

import copy
from .pieces import Pawn, Rook, Knight, Bishop, Queen, King
from .constants import BOARD_SIZE, PLAYER_WHITE, PLAYER_BLACK

class ChessBoard:
    """Represents the chess board and manages game state"""
    
    def __init__(self):
        """Initialize an empty chess board"""
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = PLAYER_WHITE
        self.move_history = []
        self.captured_pieces = []
        self.game_over = False
        self.winner = None
        self.check_status = {PLAYER_WHITE: False, PLAYER_BLACK: False}
        
        # Initialize the board with starting pieces
        self._setup_initial_position()
    
    def _setup_initial_position(self):
        """Set up the initial chess position"""
        # Place pawns
        for col in range(BOARD_SIZE):
            self.board[1][col] = Pawn(PLAYER_BLACK, 1, col)
            self.board[6][col] = Pawn(PLAYER_WHITE, 6, col)
        
        # Place other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for col, piece_class in enumerate(piece_order):
            # Black pieces
            self.board[0][col] = piece_class(PLAYER_BLACK, 0, col)
            # White pieces
            self.board[7][col] = piece_class(PLAYER_WHITE, 7, col)
    
    def get_piece(self, row, col):
        """Get the piece at the specified position"""
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.board[row][col]
        return None
    
    def set_piece(self, row, col, piece):
        """Set a piece at the specified position"""
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.board[row][col] = piece
            if piece:
                piece.row = row
                piece.col = col
    
    def remove_piece(self, row, col):
        """Remove the piece at the specified position"""
        piece = self.get_piece(row, col)
        if piece:
            self.board[row][col] = None
        return piece
    
    def move_piece(self, from_row, from_col, to_row, to_col, promotion_piece=None):
        """
        Move a piece from one position to another
        
        Args:
            from_row, from_col: Source position
            to_row, to_col: Target position
            promotion_piece: Type of piece for pawn promotion (Queen, Rook, Bishop, Knight)
        
        Returns:
            bool: True if move was successful, False otherwise
        """
        piece = self.get_piece(from_row, from_col)
        if not piece or piece.color != self.current_player:
            return False
        
        # Validate the move
        if not piece.can_move_to(to_row, to_col, self):
            return False
        
        # Check if move would put own king in check
        if self.would_be_in_check(self.current_player, from_row, from_col, to_row, to_col):
            return False
        
        # Record the move for history
        captured_piece = self.get_piece(to_row, to_col)
        move_data = {
            'from': (from_row, from_col),
            'to': (to_row, to_col),
            'piece': piece.__class__.__name__,
            'captured': captured_piece.__class__.__name__ if captured_piece else None,
            'player': self.current_player
        }
        
        # Handle special moves
        special_move_data = self._handle_special_moves(piece, from_row, from_col, to_row, to_col)
        if special_move_data:
            move_data.update(special_move_data)
        
        # Perform the move
        if captured_piece:
            self.captured_pieces.append(captured_piece)
        
        self.set_piece(to_row, to_col, piece)
        self.set_piece(from_row, from_col, None)
        piece.move(to_row, to_col)
        
        # Handle pawn promotion
        if isinstance(piece, Pawn) and piece.is_promoting():
            if promotion_piece:
                promoted_piece = promotion_piece(piece.color, to_row, to_col)
                promoted_piece.has_moved = True
                self.set_piece(to_row, to_col, promoted_piece)
                move_data['promotion'] = promotion_piece.__name__
            else:
                # Default to Queen if no promotion piece specified
                queen = Queen(piece.color, to_row, to_col)
                queen.has_moved = True
                self.set_piece(to_row, to_col, queen)
                move_data['promotion'] = 'Queen'
        
        # Clear en passant vulnerability for all pawns except the one that just moved
        self._update_en_passant_status(piece)
        
        self.move_history.append(move_data)
        
        # Switch players
        self.current_player = PLAYER_BLACK if self.current_player == PLAYER_WHITE else PLAYER_WHITE
        
        # Update check status
        self._update_check_status()
        
        # Check for game over conditions
        self._check_game_over()
        
        return True
    
    def _handle_special_moves(self, piece, from_row, from_col, to_row, to_col):
        """Handle special moves like castling and en passant"""
        special_data = {}
        
        # Castling
        if isinstance(piece, King) and abs(to_col - from_col) == 2:
            if to_col > from_col:  # Kingside castling
                rook = self.get_piece(from_row, 7)
                self.set_piece(from_row, to_col - 1, rook)
                self.set_piece(from_row, 7, None)
                rook.move(from_row, to_col - 1)
                special_data['castling'] = 'kingside'
            else:  # Queenside castling
                rook = self.get_piece(from_row, 0)
                self.set_piece(from_row, to_col + 1, rook)
                self.set_piece(from_row, 0, None)
                rook.move(from_row, to_col + 1)
                special_data['castling'] = 'queenside'
        
        # En passant
        elif isinstance(piece, Pawn):
            if abs(to_col - from_col) == 1 and self.get_piece(to_row, to_col) is None:
                # This is en passant capture
                captured_pawn = self.get_piece(from_row, to_col)
                if captured_pawn:
                    self.captured_pieces.append(captured_pawn)
                    self.set_piece(from_row, to_col, None)
                    special_data['en_passant'] = True
        
        return special_data
    
    def _update_en_passant_status(self, moved_piece):
        """Update en passant vulnerability status for all pawns"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if isinstance(piece, Pawn):
                    if piece != moved_piece:
                        piece.en_passant_vulnerable = False
    
    def is_in_check(self, color):
        """Check if the specified color's king is in check"""
        king_pos = self._find_king(color)
        if not king_pos:
            return False
        
        return self._is_square_attacked(king_pos[0], king_pos[1], color)
    
    def would_be_in_check(self, color, from_row, from_col, to_row, to_col):
        """Check if a move would put the king in check"""
        # Create a temporary board state
        temp_board = self._create_board_copy()
        
        # Perform the temporary move
        piece = temp_board.get_piece(from_row, from_col)
        captured = temp_board.get_piece(to_row, to_col)
        temp_board.set_piece(to_row, to_col, piece)
        temp_board.set_piece(from_row, from_col, None)
        if piece:
            piece.row = to_row
            piece.col = to_col
        
        # Check if king would be in check
        result = temp_board.is_in_check(color)
        
        return result
    
    def _is_square_attacked(self, row, col, defending_color):
        """Check if a square is attacked by the opposing color"""
        attacking_color = PLAYER_BLACK if defending_color == PLAYER_WHITE else PLAYER_WHITE
        
        for board_row in range(BOARD_SIZE):
            for board_col in range(BOARD_SIZE):
                piece = self.get_piece(board_row, board_col)
                if piece and piece.color == attacking_color:
                    if piece.can_move_to(row, col, self):
                        return True
        
        return False
    
    def _find_king(self, color):
        """Find the position of the king for the specified color"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None
    
    def _update_check_status(self):
        """Update the check status for both players"""
        self.check_status[PLAYER_WHITE] = self.is_in_check(PLAYER_WHITE)
        self.check_status[PLAYER_BLACK] = self.is_in_check(PLAYER_BLACK)
    
    def _check_game_over(self):
        """Check for checkmate or stalemate conditions"""
        if self._is_checkmate(self.current_player):
            self.game_over = True
            self.winner = PLAYER_BLACK if self.current_player == PLAYER_WHITE else PLAYER_WHITE
        elif self._is_stalemate(self.current_player):
            self.game_over = True
            self.winner = None  # Draw
    
    def _is_checkmate(self, color):
        """Check if the specified color is in checkmate"""
        if not self.is_in_check(color):
            return False
        
        return not self._has_legal_moves(color)
    
    def _is_stalemate(self, color):
        """Check if the specified color is in stalemate"""
        if self.is_in_check(color):
            return False
        
        return not self._has_legal_moves(color)
    
    def _has_legal_moves(self, color):
        """Check if the specified color has any legal moves"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    for move_row, move_col in piece.get_valid_moves(self):
                        if not self.would_be_in_check(color, row, col, move_row, move_col):
                            return True
        return False
    
    def get_all_legal_moves(self, color):
        """Get all legal moves for the specified color"""
        legal_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    for move_row, move_col in piece.get_valid_moves(self):
                        if not self.would_be_in_check(color, row, col, move_row, move_col):
                            legal_moves.append(((row, col), (move_row, move_col)))
        return legal_moves
    
    def _create_board_copy(self):
        """Create a deep copy of the current board state"""
        board_copy = ChessBoard()
        board_copy.current_player = self.current_player
        board_copy.check_status = self.check_status.copy()
        
        # Copy all pieces
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if piece:
                    piece_copy = piece.copy()
                    board_copy.set_piece(row, col, piece_copy)
                else:
                    board_copy.set_piece(row, col, None)
        
        return board_copy
    
    def get_board_state(self):
        """Get a string representation of the board state"""
        state = ""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if piece:
                    state += piece.get_piece_symbol()
                else:
                    state += "."
        return state
    
    def print_board(self):
        """Print a text representation of the board (for debugging)"""
        print("  a b c d e f g h")
        for row in range(BOARD_SIZE):
            print(f"{8-row} ", end="")
            for col in range(BOARD_SIZE):
                piece = self.get_piece(row, col)
                if piece:
                    print(piece.get_piece_symbol(), end=" ")
                else:
                    print(".", end=" ")
            print(f" {8-row}")
        print("  a b c d e f g h")