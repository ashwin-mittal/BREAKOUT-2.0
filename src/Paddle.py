# TESTED.

import random

import constants
from Util import keysPressed
from Window import window


class Paddle:
    def __init__(self):
        self.paddle = 1

        self.dx = 0

        self.width = 16
        self.height = 2

        self.isGrab = 0

        self.change = 1

        self.bulleted = 0
        self.bulletedTime = 0

        self.x = (constants.WINDOW_WIDTH - self.width) // 2
        self.y = constants.WINDOW_HEIGHT - self.height - constants.GROUND_HEIGHT

        self.skin = random.choice(range(len(constants.COLORS)))

    def resize(self, change, balls):
        self.change += change
        newPaddle = max(0, min(2, self.change))
        self.paddle = newPaddle
        self.width = 10 + newPaddle * 6

        self.x = min(self.x, constants.WINDOW_WIDTH - self.width)

        for ball in balls:
            if ball.dx == 0 and ball.dy == 0:
                ball.x = min(ball.x, self.x + self.width)

    def resetSize(self):
        self.change = 1
        self.paddle = 1
        self.width = 16

        self.isGrab = 0
        self.bulleted = 0

        self.x = min(self.x, constants.WINDOW_WIDTH - self.width)

    def update(self, balls=None):
        if balls is None:
            balls = []
        if "a" in keysPressed:
            self.dx = -constants.PADDLE_SPEED
        elif "d" in keysPressed:
            self.dx = constants.PADDLE_SPEED
        else:
            self.dx = 0

        previousX = self.x

        if self.dx < 0:
            self.x = max(0, self.x + self.dx)
        else:
            self.x = min(constants.WINDOW_WIDTH - self.width, self.x + self.dx)

        for ball in balls:
            if ball.dx == 0 and ball.dy == 0:
                ball.x += self.x - previousX

    def render(self):
        if self.bulleted:
            window.draw(
                constants.GUN_PADDLES[self.paddle],
                self.skin,
                self.x,
                self.y,
            )
        else:
            window.draw(
                constants.PADDLES[self.paddle],
                self.skin,
                self.x,
                self.y,
            )
