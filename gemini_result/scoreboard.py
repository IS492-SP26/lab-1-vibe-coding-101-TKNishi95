import pygame
from constants import *

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player1_score = 0
        self.player2_score = 0
        self.font = pygame.font.Font(None, 50)
        self.update_text()

    def update_text(self):
        self.image = self.font.render(f"{self.player1_score} | {self.player2_score}", True, WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 30))

    def player1_point(self):
        self.player1_score += 1
        self.update_text()

    def player2_point(self):
        self.player2_score += 1
        self.update_text()
