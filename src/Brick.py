# Brick Class.
import random

import constants
from Window import window


class Brick:
    def __init__(self, x, y):
        # Used for coloring and
        # score calculation.
        self.color = 0

        self.x = x
        self.y = y
        self.width = 7
        self.height = 3

        self.inPlay = True

        # 0 means unbreakable.
        # 1 means breakable.
        self.type = random.choices(
            (0, 1), weights=(constants.PROBABILITY, 1 - constants.PROBABILITY)
        )[0]

        self.change = 0
        if self.type:
            self.change = random.choices(
                (0, 1), weights=(1 - constants.PROBABILITY, constants.PROBABILITY)
            )[0]

        self.lastTime = 0

    def hit(self):
        if self.type:
            if self.color > 0:
                self.color -= 1
            else:
                self.inPlay = False

    def update(self, dt):
        self.lastTime += dt
        if self.change and self.lastTime >= 0.05:
            self.color = random.choice(range(1, len(constants.COLORS)))
            self.lastTime = 0

    def render(self):
        if self.inPlay:
            window.draw(
                constants.BRICK if self.type else constants.UNBREAKABLE_BRICK,
                self.color,
                self.x,
                self.y,
            )
