# Powerup Class.
from Window import window
from constants import POWERUPS, WINDOW_WIDTH

GRAVITY = 0.2


class Powerup:
    def __init__(self, brick, kind, dx, dy):
        self.x = brick.x
        self.y = brick.y

        self.height = brick.height
        self.width = brick.width

        self.dx = dx
        self.dy = dy

        self.type = kind

        self.inPlay = True

    def collides(self, target):
        if self.x > target.x + target.width or target.x > self.x + self.width:
            return False

        if self.y > target.y + target.height or target.y > self.y + self.height:
            return False

        return True

    def update(self, dt):
        self.dy = self.dy + GRAVITY * dt

        self.y = self.y + self.dy
        self.x = self.x + self.dx

        if self.x <= 0:
            self.x = 0
            self.dx = -self.dx

        if self.x >= WINDOW_WIDTH - self.width:
            self.x = WINDOW_WIDTH - self.width
            self.dx = -self.dx

        if self.y <= 2:
            self.y = 2
            self.dy = -self.dy

    def render(self):
        window.draw(POWERUPS[self.type], 0, self.x, self.y)
