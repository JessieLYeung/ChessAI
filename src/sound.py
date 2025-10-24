import pygame
import os

class Sound:

    def __init__(self, path):
        self.path = path
        try:
            self.sound = pygame.mixer.Sound(path)
        except pygame.error:
            print(f"Warning: Could not load sound file {path}")
            self.sound = None

    def play(self):
        if self.sound:
            self.sound.play()
        else:
            print("Sound not available")