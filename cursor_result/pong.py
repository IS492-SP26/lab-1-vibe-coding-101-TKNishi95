"""
Simple Ping-Pong (Pong) game using Python's built-in turtle module.

Meets minimal requirements:
- Game environment: field, 2 paddles, 1 ball
- Player input: move paddles up/down
- Ball movement + collisions: bounce off walls + paddles
- Score keeping: track + display score for each player
"""

from __future__ import annotations

import random
import turtle

# ---------- Config ----------
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

PADDLE_W = 20
PADDLE_H = 120
PADDLE_STEP = 28

BALL_SIZE = 18
BALL_START_SPEED = 6.5
BALL_SPEEDUP_ON_PADDLE = 1.05

FPS = 60
FRAME_MS = int(1000 / FPS)

FG = "white"
BG = "black"


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


class Pong:
    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.title("Python Ping-Pong (Pong)")
        self.screen.bgcolor(BG)
        self.screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.screen.tracer(0)

        self.paused = False
        self.score_left = 0
        self.score_right = 0

        self._draw_center_line()
        self._create_paddles()
        self._create_ball()
        self._create_scoreboard()

        self._bind_keys()
        self._reset_round(direction=random.choice([-1, 1]))

    # ---------- Setup ----------
    def _draw_center_line(self) -> None:
        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(FG)
        pen.penup()
        pen.goto(0, WINDOW_HEIGHT // 2)
        pen.setheading(270)
        pen.pensize(3)
        dash = 18
        gap = 14
        y = WINDOW_HEIGHT // 2
        while y > -WINDOW_HEIGHT // 2:
            pen.pendown()
            pen.forward(dash)
            pen.penup()
            pen.forward(gap)
            y -= dash + gap

    def _create_paddles(self) -> None:
        x_offset = (WINDOW_WIDTH // 2) - 60
        self.paddle_left = turtle.Turtle()
        self.paddle_left.speed(0)
        self.paddle_left.shape("square")
        self.paddle_left.color(FG)
        self.paddle_left.shapesize(stretch_wid=PADDLE_H / 20, stretch_len=PADDLE_W / 20)
        self.paddle_left.penup()
        self.paddle_left.goto(-x_offset, 0)

        self.paddle_right = turtle.Turtle()
        self.paddle_right.speed(0)
        self.paddle_right.shape("square")
        self.paddle_right.color(FG)
        self.paddle_right.shapesize(stretch_wid=PADDLE_H / 20, stretch_len=PADDLE_W / 20)
        self.paddle_right.penup()
        self.paddle_right.goto(x_offset, 0)

    def _create_ball(self) -> None:
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape("square")
        self.ball.color(FG)
        self.ball.shapesize(stretch_wid=BALL_SIZE / 20, stretch_len=BALL_SIZE / 20)
        self.ball.penup()
        self.ball.goto(0, 0)

        self.ball_vx = BALL_START_SPEED
        self.ball_vy = BALL_START_SPEED * 0.6

    def _create_scoreboard(self) -> None:
        self.score_pen = turtle.Turtle(visible=False)
        self.score_pen.speed(0)
        self.score_pen.color(FG)
        self.score_pen.penup()
        self.score_pen.goto(0, (WINDOW_HEIGHT // 2) - 55)
        self._render_score()

        self.hint_pen = turtle.Turtle(visible=False)
        self.hint_pen.speed(0)
        self.hint_pen.color("#bbbbbb")
        self.hint_pen.penup()
        self.hint_pen.goto(0, -(WINDOW_HEIGHT // 2) + 20)
        self.hint_pen.write(
            "Left: W/S   Right: ↑/↓   Space: Pause/Resume   R: Reset Score   Q: Quit",
            align="center",
            font=("Courier", 12, "normal"),
        )

    def _bind_keys(self) -> None:
        self.screen.listen()
        # Left paddle
        self.screen.onkeypress(self.left_up, "w")
        self.screen.onkeypress(self.left_down, "s")
        self.screen.onkeypress(self.left_up, "W")
        self.screen.onkeypress(self.left_down, "S")
        # Right paddle
        self.screen.onkeypress(self.right_up, "Up")
        self.screen.onkeypress(self.right_down, "Down")
        # Game controls
        self.screen.onkeypress(self.toggle_pause, "space")
        self.screen.onkeypress(self.reset_score, "r")
        self.screen.onkeypress(self.reset_score, "R")
        self.screen.onkeypress(self.quit, "q")
        self.screen.onkeypress(self.quit, "Q")

    # ---------- Paddle controls ----------
    def _move_paddle(self, paddle: turtle.Turtle, dy: float) -> None:
        top = (WINDOW_HEIGHT / 2) - (PADDLE_H / 2) - 10
        bottom = -(WINDOW_HEIGHT / 2) + (PADDLE_H / 2) + 10
        new_y = clamp(paddle.ycor() + dy, bottom, top)
        paddle.sety(new_y)

    def left_up(self) -> None:
        self._move_paddle(self.paddle_left, PADDLE_STEP)

    def left_down(self) -> None:
        self._move_paddle(self.paddle_left, -PADDLE_STEP)

    def right_up(self) -> None:
        self._move_paddle(self.paddle_right, PADDLE_STEP)

    def right_down(self) -> None:
        self._move_paddle(self.paddle_right, -PADDLE_STEP)

    # ---------- Game controls ----------
    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def reset_score(self) -> None:
        self.score_left = 0
        self.score_right = 0
        self._render_score()
        self._reset_round(direction=random.choice([-1, 1]))

    def quit(self) -> None:
        self.screen.bye()

    # ---------- Ball + collisions ----------
    def _render_score(self) -> None:
        self.score_pen.clear()
        self.score_pen.write(
            f"{self.score_left}   :   {self.score_right}",
            align="center",
            font=("Courier", 28, "bold"),
        )

    def _reset_round(self, direction: int) -> None:
        """Reset ball to center and serve towards direction (-1 left, +1 right)."""
        self.ball.goto(0, 0)
        speed = BALL_START_SPEED
        self.ball_vx = speed * direction
        self.ball_vy = speed * random.choice([-0.75, -0.55, 0.55, 0.75])

    def _ball_hits_paddle(self, paddle: turtle.Turtle) -> bool:
        # Axis-aligned bounding box overlap check.
        px, py = paddle.xcor(), paddle.ycor()
        bx, by = self.ball.xcor(), self.ball.ycor()

        half_pw = PADDLE_W / 2
        half_ph = PADDLE_H / 2
        half_bs = BALL_SIZE / 2

        return (
            abs(bx - px) <= (half_pw + half_bs)
            and abs(by - py) <= (half_ph + half_bs)
        )

    def _apply_paddle_bounce(self, paddle: turtle.Turtle, direction: int) -> None:
        """
        direction: -1 means bounce to the left, +1 bounce to the right (post-collision).
        Adds a little vertical change based on where you hit the paddle.
        """
        # Put ball just outside paddle to prevent sticking.
        px = paddle.xcor()
        offset_x = (PADDLE_W / 2) + (BALL_SIZE / 2) + 2
        self.ball.setx(px + (offset_x * direction))

        # Calculate "spin" by impact position.
        impact = (self.ball.ycor() - paddle.ycor()) / (PADDLE_H / 2)
        impact = clamp(impact, -1.0, 1.0)

        self.ball_vx = abs(self.ball_vx) * direction * BALL_SPEEDUP_ON_PADDLE
        self.ball_vy = (self.ball_vy + (impact * 2.6)) * 0.98

        # Cap max speed a bit for playability.
        max_speed = 15
        self.ball_vx = clamp(self.ball_vx, -max_speed, max_speed)
        self.ball_vy = clamp(self.ball_vy, -max_speed, max_speed)

    def tick(self) -> None:
        if not self.paused:
            # Move ball
            self.ball.setx(self.ball.xcor() + self.ball_vx)
            self.ball.sety(self.ball.ycor() + self.ball_vy)

            # Bounce on top/bottom walls
            top = (WINDOW_HEIGHT / 2) - (BALL_SIZE / 2) - 6
            bottom = -(WINDOW_HEIGHT / 2) + (BALL_SIZE / 2) + 6
            if self.ball.ycor() >= top:
                self.ball.sety(top)
                self.ball_vy *= -1
            elif self.ball.ycor() <= bottom:
                self.ball.sety(bottom)
                self.ball_vy *= -1

            # Paddle collisions
            if self.ball_vx < 0 and self._ball_hits_paddle(self.paddle_left):
                self._apply_paddle_bounce(self.paddle_left, direction=+1)
            elif self.ball_vx > 0 and self._ball_hits_paddle(self.paddle_right):
                self._apply_paddle_bounce(self.paddle_right, direction=-1)

            # Scoring (ball passes left/right bounds)
            right_out = (WINDOW_WIDTH / 2) + 40
            left_out = -(WINDOW_WIDTH / 2) - 40
            if self.ball.xcor() > right_out:
                self.score_left += 1
                self._render_score()
                self._reset_round(direction=-1)
            elif self.ball.xcor() < left_out:
                self.score_right += 1
                self._render_score()
                self._reset_round(direction=+1)

        self.screen.update()
        self.screen.ontimer(self.tick, FRAME_MS)

    def run(self) -> None:
        self.tick()
        self.screen.mainloop()


def main() -> None:
    Pong().run()


if __name__ == "__main__":
    main()

