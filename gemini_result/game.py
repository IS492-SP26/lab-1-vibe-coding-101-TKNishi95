import pygame
from constants import *
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gemini Ping Pong")
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.paddles = pygame.sprite.Group()
        self.ball_sprite = pygame.sprite.GroupSingle()
        self.scoreboard_sprite = pygame.sprite.GroupSingle()
        self.setup()

    def setup(self):
        self.player1 = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.player2 = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.scoreboard = Scoreboard()

        self.all_sprites.add(self.player1, self.player2, self.ball)
        self.paddles.add(self.player1, self.player2)
        self.ball_sprite.add(self.ball)
        self.scoreboard_sprite.add(self.scoreboard)


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player1.move_up()
        if keys[pygame.K_s]:
            self.player1.move_down()
        if keys[pygame.K_UP]:
            self.player2.move_up()
        if keys[pygame.K_DOWN]:
            self.player2.move_down()

    def update(self):
        self.all_sprites.update()
        self.check_collisions()

    def check_collisions(self):
        # Ball and paddles
        if pygame.sprite.spritecollide(self.ball, self.paddles, False):
            self.ball.speed_x *= -1

        # Ball and walls
        if self.ball.rect.x >= SCREEN_WIDTH - BALL_SIZE:
            self.scoreboard.player1_point()
            self.ball.reset()

        if self.ball.rect.x <= 0:
            self.scoreboard.player2_point()
            self.ball.reset()


    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.scoreboard_sprite.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
