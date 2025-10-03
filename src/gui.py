"""
Pygame GUI interface for the chess game
"""

import pygame
import os
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, SQUARE_SIZE,
    BOARD_OFFSET_X, BOARD_OFFSET_Y, WHITE, BLACK, LIGHT_BROWN, DARK_BROWN,
    HIGHLIGHT_COLOR, SELECTED_COLOR, VALID_MOVE_COLOR, RED, FPS
)
from .pieces import Queen, Rook, Bishop, Knight

class ChessGUI:
    """Pygame GUI for the chess game"""
    
    def __init__(self):
        """Initialize the GUI"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI Chess Bot")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Selection and highlighting
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None
        
        # Promotion dialog
        self.promotion_active = False
        self.promotion_color = None
        
        # Load piece images if available
        self._load_piece_images()
    
    def _load_piece_images(self):
        """Load piece images from assets folder"""
        self.piece_images = {}
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        
        for color in colors:
            for piece in pieces:
                filename = f"{color}_{piece}.png"
                filepath = os.path.join("assets", "images", filename)
                
                if os.path.exists(filepath):
                    try:
                        image = pygame.image.load(filepath)
                        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                        self.piece_images[f"{color}_{piece}"] = image
                    except pygame.error:
                        # Use text fallback if image loading fails
                        self.piece_images[f"{color}_{piece}"] = None
                else:
                    # Image file doesn't exist, use text fallback
                    self.piece_images[f"{color}_{piece}"] = None
    
    def draw_board(self, board):
        """Draw the chess board and pieces"""
        self.screen.fill(WHITE)
        
        # Draw board squares
        for row in range(8):
            for col in range(8):
                x = BOARD_OFFSET_X + col * SQUARE_SIZE
                y = BOARD_OFFSET_Y + row * SQUARE_SIZE
                
                # Alternate square colors
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight selected square
                if self.selected_square and self.selected_square == (row, col):
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill(SELECTED_COLOR)
                    self.screen.blit(highlight_surface, (x, y))
                
                # Highlight last move
                if self.last_move:
                    if (row, col) in [self.last_move[0], self.last_move[1]]:
                        highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        highlight_surface.fill(HIGHLIGHT_COLOR)
                        self.screen.blit(highlight_surface, (x, y))
                
                # Show valid moves
                if (row, col) in self.valid_moves:
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill(VALID_MOVE_COLOR)
                    self.screen.blit(highlight_surface, (x, y))
                    
                    # Draw circle for empty squares, border for captures
                    piece = board.get_piece(row, col)
                    if piece is None:
                        pygame.draw.circle(self.screen, (0, 0, 255), 
                                         (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), 10)
                    else:
                        pygame.draw.rect(self.screen, (255, 0, 0), 
                                       (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)
        
        # Draw pieces
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    self._draw_piece(piece, row, col)
        
        # Draw board labels
        self._draw_board_labels()
        
        # Draw game information
        self._draw_game_info(board)
        
        # Draw promotion dialog if active
        if self.promotion_active:
            self._draw_promotion_dialog()
    
    def _draw_piece(self, piece, row, col):
        """Draw a single piece"""
        x = BOARD_OFFSET_X + col * SQUARE_SIZE
        y = BOARD_OFFSET_Y + row * SQUARE_SIZE
        
        piece_type = piece.__class__.__name__.lower()
        image_key = f"{piece.color}_{piece_type}"
        
        if image_key in self.piece_images:
            self.screen.blit(self.piece_images[image_key], (x, y))
        else:
            # Fallback text representation
            symbol = piece.get_piece_symbol()
            text_color = BLACK if piece.color == 'white' else WHITE
            text = self.font.render(symbol, True, text_color)
            text_rect = text.get_rect(center=(x + SQUARE_SIZE//2, y + SQUARE_SIZE//2))
            self.screen.blit(text, text_rect)
    
    def _draw_board_labels(self):
        """Draw coordinate labels around the board"""
        # File labels (a-h)
        for col in range(8):
            label = chr(ord('a') + col)
            x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = BOARD_OFFSET_Y + BOARD_HEIGHT + 10
            
            text = self.small_font.render(label, True, BLACK)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
        
        # Rank labels (1-8)
        for row in range(8):
            label = str(8 - row)
            x = BOARD_OFFSET_X - 20
            y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
            
            text = self.small_font.render(label, True, BLACK)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
    
    def _draw_game_info(self, board):
        """Draw game information panel"""
        info_x = BOARD_OFFSET_X + BOARD_WIDTH + 20
        info_y = BOARD_OFFSET_Y
        
        # Current player
        current_text = f"Current Player: {board.current_player.title()}"
        text = self.small_font.render(current_text, True, BLACK)
        self.screen.blit(text, (info_x, info_y))
        
        # Check status
        if board.check_status['white']:
            check_text = "White King in Check!"
            text = self.small_font.render(check_text, True, RED)
            self.screen.blit(text, (info_x, info_y + 30))
        
        if board.check_status['black']:
            check_text = "Black King in Check!"
            text = self.small_font.render(check_text, True, RED)
            self.screen.blit(text, (info_x, info_y + 60))
        
        # Game over status
        if board.game_over:
            if board.winner:
                winner_text = f"{board.winner.title()} Wins!"
                text = self.font.render(winner_text, True, RED)
                self.screen.blit(text, (info_x, info_y + 100))
            else:
                draw_text = "Draw!"
                text = self.font.render(draw_text, True, RED)
                self.screen.blit(text, (info_x, info_y + 100))
        
        # Move history (last few moves)
        history_y = info_y + 150
        history_text = self.small_font.render("Recent Moves:", True, BLACK)
        self.screen.blit(history_text, (info_x, history_y))
        
        for i, move in enumerate(board.move_history[-5:]):
            move_text = f"{move['piece']} {self._format_square(move['from'])} -> {self._format_square(move['to'])}"
            if move.get('captured'):
                move_text += f" (x{move['captured']})"
            
            text = self.small_font.render(move_text, True, BLACK)
            self.screen.blit(text, (info_x, history_y + 30 + i * 20))
        
        # Controls help
        controls_y = history_y + 160
        controls_text = self.small_font.render("Controls:", True, BLACK)
        self.screen.blit(controls_text, (info_x, controls_y))
        
        controls = [
            "ESC - Exit game",
            "R - Restart (when game over)",
            "S - Save game"
        ]
        
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, BLACK)
            self.screen.blit(text, (info_x, controls_y + 20 + i * 15))
    
    def _draw_promotion_dialog(self):
        """Draw pawn promotion selection dialog"""
        dialog_width = 240
        dialog_height = 80
        dialog_x = (WINDOW_WIDTH - dialog_width) // 2
        dialog_y = (WINDOW_HEIGHT - dialog_height) // 2
        
        # Background
        pygame.draw.rect(self.screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3)
        
        # Title
        title_text = self.font.render("Choose Promotion:", True, BLACK)
        title_rect = title_text.get_rect(center=(dialog_x + dialog_width//2, dialog_y + 20))
        self.screen.blit(title_text, title_rect)
        
        # Piece options
        pieces = [Queen, Rook, Bishop, Knight]
        piece_names = ['Queen', 'Rook', 'Bishop', 'Knight']
        
        for i, (piece_class, name) in enumerate(zip(pieces, piece_names)):
            piece_x = dialog_x + 20 + i * 50
            piece_y = dialog_y + 40
            
            # Draw piece icon
            if self.promotion_color:
                piece_type = piece_class.__name__.lower()
                image_key = f"{self.promotion_color}_{piece_type}"
                
                if image_key in self.piece_images:
                    piece_image = pygame.transform.scale(self.piece_images[image_key], (40, 40))
                    self.screen.blit(piece_image, (piece_x, piece_y))
                else:
                    # Fallback text
                    piece = piece_class(self.promotion_color, 0, 0)
                    symbol = piece.get_piece_symbol()
                    text = self.font.render(symbol, True, BLACK)
                    text_rect = text.get_rect(center=(piece_x + 20, piece_y + 20))
                    self.screen.blit(text, text_rect)
    
    def _format_square(self, pos):
        """Format a position tuple as chess notation"""
        row, col = pos
        return f"{chr(ord('a') + col)}{8 - row}"
    
    def get_square_from_mouse(self, mouse_pos):
        """Convert mouse position to board square coordinates"""
        x, y = mouse_pos
        
        # Check if click is within the board
        if (BOARD_OFFSET_X <= x < BOARD_OFFSET_X + BOARD_WIDTH and
            BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + BOARD_HEIGHT):
            
            col = (x - BOARD_OFFSET_X) // SQUARE_SIZE
            row = (y - BOARD_OFFSET_Y) // SQUARE_SIZE
            
            if 0 <= row < 8 and 0 <= col < 8:
                return (row, col)
        
        return None
    
    def handle_square_click(self, square, board):
        """Handle clicking on a board square"""
        if board.game_over:
            return None
        
        row, col = square
        
        # If no square selected, select this square if it has a piece of current player
        if self.selected_square is None:
            piece = board.get_piece(row, col)
            if piece and piece.color == board.current_player:
                self.selected_square = square
                self.valid_moves = piece.get_valid_moves(board)
                # Filter out moves that would put king in check
                self.valid_moves = [
                    move for move in self.valid_moves
                    if not board.would_be_in_check(piece.color, piece.row, piece.col, move[0], move[1])
                ]
        
        # If square is selected, try to move
        elif self.selected_square:
            if square == self.selected_square:
                # Deselect
                self.selected_square = None
                self.valid_moves = []
            elif square in self.valid_moves:
                # Make the move
                from_row, from_col = self.selected_square
                to_row, to_col = square
                
                piece = board.get_piece(from_row, from_col)
                
                # Check for pawn promotion
                if (isinstance(piece, type(board.get_piece(from_row, from_col))) and 
                    piece.__class__.__name__ == 'Pawn' and
                    ((piece.color == 'white' and to_row == 0) or 
                     (piece.color == 'black' and to_row == 7))):
                    
                    # Start promotion dialog
                    self.promotion_active = True
                    self.promotion_color = piece.color
                    return ('promote', from_row, from_col, to_row, to_col)
                
                # Regular move
                if board.move_piece(from_row, from_col, to_row, to_col):
                    self.last_move = (self.selected_square, square)
                    self.selected_square = None
                    self.valid_moves = []
                    return ('move', from_row, from_col, to_row, to_col)
            else:
                # Try to select new piece
                piece = board.get_piece(row, col)
                if piece and piece.color == board.current_player:
                    self.selected_square = square
                    self.valid_moves = piece.get_valid_moves(board)
                    # Filter out moves that would put king in check
                    self.valid_moves = [
                        move for move in self.valid_moves
                        if not board.would_be_in_check(piece.color, piece.row, piece.col, move[0], move[1])
                    ]
                else:
                    self.selected_square = None
                    self.valid_moves = []
        
        return None
    
    def handle_promotion_click(self, mouse_pos, pending_move):
        """Handle clicking on promotion dialog"""
        if not self.promotion_active:
            return None
        
        dialog_width = 240
        dialog_height = 80
        dialog_x = (WINDOW_WIDTH - dialog_width) // 2
        dialog_y = (WINDOW_HEIGHT - dialog_height) // 2
        
        piece_y = dialog_y + 40
        pieces = [Queen, Rook, Bishop, Knight]
        
        for i, piece_class in enumerate(pieces):
            piece_x = dialog_x + 20 + i * 50
            
            if (piece_x <= mouse_pos[0] < piece_x + 40 and
                piece_y <= mouse_pos[1] < piece_y + 40):
                
                self.promotion_active = False
                self.promotion_color = None
                return piece_class
        
        return None
    
    def clear_selection(self):
        """Clear current selection and highlights"""
        self.selected_square = None
        self.valid_moves = []
    
    def update_display(self):
        """Update the pygame display"""
        pygame.display.flip()
        self.clock.tick(FPS)