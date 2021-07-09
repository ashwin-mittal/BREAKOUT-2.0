# Ball Class.
import random

import Window
import constants


class Ball:
    def __init__(self):
        self.width = 1
        self.height = 1

        # These variables are for keeping track of our velocity on both
        # the X and Y axis, since the ball can move in two dimensions.
        self.dy = 0
        self.dx = 0

        self.x = 0
        self.y = 0

        self.beforeGrabingdx = 0
        self.beforeGrabingdy = 0

        self.isThru = 0
        self.isFire = 0

        self.powerups = set()

        self.skin = random.choice(range(len(constants.COLORS)))

    def collides(self, target):
        # First, check to see if the left edge of either is
        # farther to the right than the right edge of the other.
        if self.x > target.x + target.width or target.x > self.x + self.width:
            return False

        # Then check to see if the bottom edge of either
        # is higher than the top edge of the other.
        if self.y > target.y + target.height or target.y > self.y + self.height:
            return False

        # If the above aren't true, they're overlapping.
        return True

    def update(self, dt):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        if self.x <= 0:
            self.x = 0
            self.dx = -self.dx

        if self.x >= constants.WINDOW_WIDTH - self.width:
            self.x = constants.WINDOW_WIDTH - self.width
            self.dx = -self.dx

        if self.y <= 2:
            self.y = 2
            self.dy = -self.dy

    def render(self):
        Window.window.draw(constants.BALL, self.skin, self.x, self.y)
