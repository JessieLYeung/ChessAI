"""
Simple piece image generator for when image files are not available
"""

import pygame
import os
from .constants import SQUARE_SIZE

class PieceImageGenerator:
    """Generate simple piece images programmatically"""
    
    @staticmethod
    def generate_piece_images():
        """Generate simple piece images and save them"""
        if not os.path.exists("assets/images"):
            os.makedirs("assets/images")
        
        pieces = {
            'pawn': '♟',
            'rook': '♜',
            'knight': '♞',
            'bishop': '♝',
            'queen': '♛',
            'king': '♚'
        }
        
        colors = {'white': (255, 255, 255), 'black': (0, 0, 0)}
        
        for color_name, color in colors.items():
            for piece_name, symbol in pieces.items():
                surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                
                # Draw a colored circle background
                bg_color = (240, 240, 240) if color_name == 'white' else (60, 60, 60)
                pygame.draw.circle(surface, bg_color, 
                                 (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 
                                 SQUARE_SIZE // 2 - 5)
                pygame.draw.circle(surface, (0, 0, 0), 
                                 (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 
                                 SQUARE_SIZE // 2 - 5, 2)
                
                # Try to render Unicode chess symbols
                try:
                    font = pygame.font.Font(None, SQUARE_SIZE - 10)
                    text = font.render(symbol, True, color)
                    text_rect = text.get_rect(center=(SQUARE_SIZE // 2, SQUARE_SIZE // 2))
                    surface.blit(text, text_rect)
                except:
                    # Fallback to simple shapes
                    PieceImageGenerator._draw_simple_piece(surface, piece_name, color)
                
                # Save the image
                filename = f"{color_name}_{piece_name}.png"
                filepath = os.path.join("assets", "images", filename)
                pygame.image.save(surface, filepath)
    
    @staticmethod
    def _draw_simple_piece(surface, piece_name, color):
        """Draw simple geometric shapes for pieces"""
        center_x, center_y = SQUARE_SIZE // 2, SQUARE_SIZE // 2
        
        if piece_name == 'pawn':
            pygame.draw.circle(surface, color, (center_x, center_y - 5), 8)
            pygame.draw.rect(surface, color, (center_x - 6, center_y + 3, 12, 8))
        
        elif piece_name == 'rook':
            pygame.draw.rect(surface, color, (center_x - 10, center_y - 8, 20, 16))
            pygame.draw.rect(surface, color, (center_x - 12, center_y - 12, 6, 8))
            pygame.draw.rect(surface, color, (center_x - 3, center_y - 12, 6, 8))
            pygame.draw.rect(surface, color, (center_x + 6, center_y - 12, 6, 8))
        
        elif piece_name == 'knight':
            points = [(center_x - 8, center_y + 8), (center_x - 6, center_y - 8),
                     (center_x + 2, center_y - 10), (center_x + 8, center_y - 6),
                     (center_x + 10, center_y + 8)]
            pygame.draw.polygon(surface, color, points)
        
        elif piece_name == 'bishop':
            pygame.draw.circle(surface, color, (center_x, center_y - 6), 6)
            pygame.draw.polygon(surface, color, [(center_x - 8, center_y + 8),
                                               (center_x, center_y - 2),
                                               (center_x + 8, center_y + 8)])
        
        elif piece_name == 'queen':
            pygame.draw.circle(surface, color, (center_x, center_y), 10)
            for i in range(8):
                angle = i * 45
                x = center_x + 12 * pygame.math.Vector2(1, 0).rotate(angle).x
                y = center_y + 12 * pygame.math.Vector2(1, 0).rotate(angle).y
                pygame.draw.circle(surface, color, (int(x), int(y)), 3)
        
        elif piece_name == 'king':
            pygame.draw.circle(surface, color, (center_x, center_y), 10)
            pygame.draw.rect(surface, color, (center_x - 2, center_y - 15, 4, 10))
            pygame.draw.rect(surface, color, (center_x - 6, center_y - 13, 12, 4))