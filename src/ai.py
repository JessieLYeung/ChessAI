"""
AI implementation using minimax algorithm with alpha-beta pruning
"""

import random
from .constants import (
    PIECE_VALUES, PAWN_TABLE, KNIGHT_TABLE, BISHOP_TABLE, 
    ROOK_TABLE, QUEEN_TABLE, KING_TABLE, PLAYER_WHITE, PLAYER_BLACK
)
from .pieces import Pawn, Rook, Knight, Bishop, Queen, King

class ChessAI:
    """AI player using minimax algorithm with alpha-beta pruning"""
    
    def __init__(self, color, difficulty=3):
        """
        Initialize the AI
        
        Args:
            color (str): 'white' or 'black'
            difficulty (int): Search depth (1-5, higher is stronger but slower)
        """
        self.color = color
        self.difficulty = max(1, min(5, difficulty))  # Clamp between 1-5
        self.opponent_color = PLAYER_BLACK if color == PLAYER_WHITE else PLAYER_WHITE
        
    def get_best_move(self, board):
        """
        Get the best move using minimax algorithm
        
        Args:
            board: Chess board object
            
        Returns:
            tuple: ((from_row, from_col), (to_row, to_col)) or None if no moves
        """
        legal_moves = board.get_all_legal_moves(self.color)
        
        if not legal_moves:
            return None
        
        # If only one move available, return it immediately
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        best_move = None
        best_score = float('-inf') if self.color == PLAYER_WHITE else float('inf')
        
        # Randomize move order to add variety
        random.shuffle(legal_moves)
        
        for move in legal_moves:
            from_pos, to_pos = move
            
            # Create a board copy and make the move
            board_copy = board._create_board_copy()
            piece = board_copy.get_piece(from_pos[0], from_pos[1])
            board_copy.move_piece(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
            
            # Evaluate the position
            if self.color == PLAYER_WHITE:
                score = self._minimax(board_copy, self.difficulty - 1, float('-inf'), float('inf'), False)
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                score = self._minimax(board_copy, self.difficulty - 1, float('-inf'), float('inf'), True)
                if score < best_score:
                    best_score = score
                    best_move = move
        
        return best_move
    
    def _minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning
        
        Args:
            board: Chess board object
            depth (int): Remaining search depth
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): True if maximizing player's turn
            
        Returns:
            float: Evaluation score
        """
        # Base case: reached depth limit or game over
        if depth == 0 or board.game_over:
            return self._evaluate_position(board)
        
        current_color = PLAYER_WHITE if maximizing_player else PLAYER_BLACK
        legal_moves = board.get_all_legal_moves(current_color)
        
        # No legal moves - checkmate or stalemate
        if not legal_moves:
            if board.is_in_check(current_color):
                # Checkmate - heavily penalize
                return -10000 if maximizing_player else 10000
            else:
                # Stalemate - neutral
                return 0
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                from_pos, to_pos = move
                
                # Make move on copy
                board_copy = board._create_board_copy()
                board_copy.move_piece(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
                
                eval_score = self._minimax(board_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Alpha-beta pruning
            
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                from_pos, to_pos = move
                
                # Make move on copy
                board_copy = board._create_board_copy()
                board_copy.move_piece(from_pos[0], from_pos[1], to_pos[0], to_pos[1])
                
                eval_score = self._minimax(board_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha-beta pruning
            
            return min_eval
    
    def _evaluate_position(self, board):
        """
        Evaluate the current board position
        
        Args:
            board: Chess board object
            
        Returns:
            float: Position evaluation score (positive favors white, negative favors black)
        """
        if board.game_over:
            if board.winner == PLAYER_WHITE:
                return 10000
            elif board.winner == PLAYER_BLACK:
                return -10000
            else:
                return 0  # Draw
        
        score = 0
        
        # Material and positional evaluation
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    piece_value = self._get_piece_value(piece, row, col)
                    if piece.color == PLAYER_WHITE:
                        score += piece_value
                    else:
                        score -= piece_value
        
        # King safety
        score += self._evaluate_king_safety(board, PLAYER_WHITE) * 50
        score -= self._evaluate_king_safety(board, PLAYER_BLACK) * 50
        
        # Control of center
        score += self._evaluate_center_control(board, PLAYER_WHITE) * 10
        score -= self._evaluate_center_control(board, PLAYER_BLACK) * 10
        
        # Mobility (number of legal moves)
        white_moves = len(board.get_all_legal_moves(PLAYER_WHITE))
        black_moves = len(board.get_all_legal_moves(PLAYER_BLACK))
        score += (white_moves - black_moves) * 2
        
        return score
    
    def _get_piece_value(self, piece, row, col):
        """Get the value of a piece including positional bonus"""
        piece_type = piece.__class__.__name__.lower()
        base_value = PIECE_VALUES.get(piece_type, 0)
        
        # Get positional bonus
        positional_bonus = 0
        if isinstance(piece, Pawn):
            table = PAWN_TABLE
        elif isinstance(piece, Knight):
            table = KNIGHT_TABLE
        elif isinstance(piece, Bishop):
            table = BISHOP_TABLE
        elif isinstance(piece, Rook):
            table = ROOK_TABLE
        elif isinstance(piece, Queen):
            table = QUEEN_TABLE
        elif isinstance(piece, King):
            table = KING_TABLE
        else:
            table = None
        
        if table:
            # Flip row for black pieces
            table_row = row if piece.color == PLAYER_WHITE else 7 - row
            if 0 <= table_row < 8 and 0 <= col < 8:
                positional_bonus = table[table_row][col]
        
        return base_value + positional_bonus
    
    def _evaluate_king_safety(self, board, color):
        """Evaluate king safety"""
        king_pos = board._find_king(color)
        if not king_pos:
            return -100  # King missing - very bad
        
        safety_score = 0
        king_row, king_col = king_pos
        
        # Penalize king exposure in the center early in the game
        if 2 <= king_row <= 5 and 2 <= king_col <= 5:
            safety_score -= 20
        
        # Check for pieces defending the king
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                if row_offset == 0 and col_offset == 0:
                    continue
                
                check_row = king_row + row_offset
                check_col = king_col + col_offset
                
                if 0 <= check_row < 8 and 0 <= check_col < 8:
                    piece = board.get_piece(check_row, check_col)
                    if piece and piece.color == color:
                        safety_score += 5
        
        return safety_score
    
    def _evaluate_center_control(self, board, color):
        """Evaluate control of center squares"""
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        control_score = 0
        
        for center_row, center_col in center_squares:
            piece = board.get_piece(center_row, center_col)
            if piece and piece.color == color:
                control_score += 3
            
            # Check if color attacks this center square
            if board._is_square_attacked(center_row, center_col, 
                                       PLAYER_BLACK if color == PLAYER_WHITE else PLAYER_WHITE):
                control_score += 1
        
        return control_score