# TESTED.
import random

import constants
from Bomb import Bomb
from Window import window
from src.Brick import Brick


class BossEnemy:
    def __init__(self, skin):
        self.width = 16
        self.height = 5
        self.health = constants.BOSS_ENEMY_HEALTH

        self.x = 0
        self.y = 2

        self.spawns = 2
        self.skin = skin

        self.lastTime = 0

    def collides(self, target):
        if self.health <= 0:
            return False

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

    def update(self, paddle, bombs, dt):
        if self.health <= 0:
            return

        self.lastTime += dt
        self.x = paddle.x
        if self.lastTime >= 5 and bombs is not None:
            bombs.append(
                Bomb(
                    self.x + (self.width - 6) // 2,
                    self.y + self.height,
                    self.skin,
                )
            )
            self.lastTime = 0

    def spawn(self, bricks):
        self.spawns -= 1
        for brick in bricks[:]:
            if brick.type:
                bricks.remove(brick)
        numCols = constants.WINDOW_WIDTH // 7
        for x in range(numCols):
            b = Brick(
                x * 7,
                self.height + 2,
            )
            b.color = random.choice(range(1, len(constants.COLORS)))
            b.type = 1
            b.change = 0
            bricks.append(b)

    def render(self):
        if self.health > 0:
            window.draw(
                constants.UFO,
                self.skin,
                self.x,
                self.y,
            )
