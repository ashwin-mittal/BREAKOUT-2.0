# TESTED.

import sys

import numpy as np

import constants


# -----------------
# --------------@@@
# --------------@@@
# --------------@@@

# Given (x, y).
# Maximum (self.width, self.height).
# x -> self.width.
# y -> self.height.

# @@@@
# @@@@
# @@@@
# @@@@


class Window:
    def __init__(self):
        self.width, self.height = constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT
        self.reset()

    def reset(self):
        self.colors = np.full((self.height, self.width), 0)
        self.frame = np.full((self.height, self.width), " ")
        self.frame[[-1, 1], :] = np.full((1, self.width), "X")
        self.colors[-1, :] = np.full((1, self.width), 2)
        self.colors[1, :] = np.full((1, self.width), 4)

    def draw(self, sprite, color, x: int, y: int):
        x = int(x)
        y = int(y)
        startX = 0 if x >= 0 else abs(x)
        startY = 0 if y >= 0 else abs(y)
        x = max(x, 0)
        y = max(y, 0)
        sprite = sprite.strip("\n")
        sprite = np.array([list(v) for v in sprite.split("\n")])
        sprite = sprite[
                 startY: startY + max(0, self.height - y),
                 startX: startX + max(0, self.width - x),
                 ]
        self.frame[y: y + sprite.shape[0], x: x + sprite.shape[1]] = sprite
        self.colors[y: y + sprite.shape[0], x: x + sprite.shape[1]] = color

    def display(self):
        sys.stdout.write(
            "\n".join(
                "".join(
                    constants.COLORS[c] + v
                    for (c, v) in zip(self.colors[i], self.frame[i])
                )
                for i in range(len(self.frame))
            )
        )


window = Window()
