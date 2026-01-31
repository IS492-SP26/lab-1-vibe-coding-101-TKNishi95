import pygame
from constants import *

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.reset()

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y


    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y > SCREEN_HEIGHT - BALL_SIZE or self.rect.y < 0:
            self.speed_y = -self.speed_y
