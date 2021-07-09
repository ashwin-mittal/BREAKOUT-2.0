# Ball Class.

import Window
import constants


class Bomb:
    def __init__(self, x, y, skin):
        self.width = 6
        self.height = 5

        # These variables are for keeping track of our velocity on both
        # the X and Y axis, since the ball can move in two dimensions.
        self.dy = 0.25

        self.x = x
        self.y = y

        self.skin = skin

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

    def update(self):
        self.y = self.y + self.dy

    def render(self):
        Window.window.draw(constants.BOMB, self.skin, self.x, self.y)
