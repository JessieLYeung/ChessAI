import pygame

from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    # blit method

    def update_blit(self, surface):
        # texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # img
        try:
            img = pygame.image.load(texture)
            # rect
            img_center = (self.mouseX, self.mouseY)
            self.piece.texture_rect = img.get_rect(center=img_center)
            # blit
            surface.blit(img, self.piece.texture_rect)
        except pygame.error:
            print(f"Warning: Could not load dragged piece image {texture}")
            # Draw a placeholder circle for dragged piece
            color = (255, 0, 0) if self.piece.color == 'red' else (0, 0, 255)  # fallback colors
            pygame.draw.circle(surface, color, (self.mouseX, self.mouseY), 30)

    # other methods

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos # (xcor, ycor)

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
