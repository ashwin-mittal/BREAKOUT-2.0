import os
import signal

import colorama

import Paddle
from BricksMaker import BricksMaker
from GameOverState import GameOverState
from PlayState import PlayState
from ServeState import ServeState
from StateMachine import StateMachine
from Util import keysPressed
from Window import window
from input import KBHit


def resetCursor():
    print("\033[0;0H", end="")


def getKeystrokes(keys):
    while keys.kbhit():
        keysPressed.add(keys.getch())


class Breakout:
    def __init__(self):
        os.system("clear")
        os.system("setterm -cursor off")

        signal.signal(signal.SIGINT, signal.SIG_IGN)

        colorama.init(autoreset=True)

        keys = KBHit()

        gStateMachine = StateMachine(
            {
                "serve": lambda: ServeState(),
                "play": lambda: PlayState(),
                "game-over": lambda: GameOverState(),
            }
        )

        params = {
            "level": 0,
            "paddle": Paddle.Paddle(),
            "bricks": BricksMaker.createBricks(0),
            "health": 20,
            "score": 0,
            "gStateMachine": gStateMachine,
        }

        gStateMachine.change("serve", params)

        while True:
            getKeystrokes(keys)
            resetCursor()
            window.reset()
            gStateMachine.update()
            gStateMachine.render()
            window.display()
            keysPressed.clear()

    def __del__(self):
        os.system("setterm -cursor on")
