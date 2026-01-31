import pygame
from constants import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_up(self):
        if self.rect.y > 0:
            self.rect.y -= PADDLE_SPEED

    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            self.rect.y += PADDLE_SPEED
