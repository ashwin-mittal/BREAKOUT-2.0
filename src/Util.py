# TESTED.

import time

from Window import window
from constants import WINDOW_WIDTH

# A set we'll use to keep track of which
# keys have been pressed this frame.
keysPressed = set()


def renderHealth(health):
    _health = "{BREAKOUT}{♥: %d}" % health
    window.draw(_health, 0, (WINDOW_WIDTH - len(_health)) // 2, 0)


def renderScore(score):
    _score = "{SCORE: %d}" % score
    window.draw(_score, 0, 0, 0)


def renderLevel(level):
    _level = "{LEVEL: %d}" % level
    window.draw(_level, 0, 0, 1)


def renderPowerupTime(remaining_time):
    _time = "{LASERS: %d}" % remaining_time
    window.draw(_time, 0, WINDOW_WIDTH - len(_time), 1)


def renderEnemyHealth(health):
    _health = f"{{ENEMY: {''.join('█' for _ in range(health))}}}"
    window.draw(_health, 0, (WINDOW_WIDTH - len(_health)) // 2, 1)


class Timer:
    def __init__(self):
        self.start = time.time()

    def getTime(self):
        return int(time.time() - self.start)

    def render(self):
        _time = "{TIME: %0.1f}" % (time.time() - self.start)
        window.draw(_time, 0, WINDOW_WIDTH - len(_time), 0)


def checkExit(gStateMachine, score):
    if "q" in keysPressed:
        gStateMachine.change("game-over", {"score": score, "victory": False})
