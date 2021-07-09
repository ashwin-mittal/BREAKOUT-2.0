# GameOverState Class.
import sys

import Paddle
from BaseState import BaseState
from BricksMaker import BricksMaker
from Util import checkExit, keysPressed, renderScore
from Window import window
from constants import GAME_OVER, GAME_WON, LAST_LEVEL, WINDOW_HEIGHT, WINDOW_WIDTH


class GameOverState(BaseState):
    def enter(self, params):
        self.level = params.get("level", 0)
        self.health = params.get("health", 0)
        self.score = params.get("score", 0)
        self.victory = params["victory"]
        self.gStateMachine = params.get("gStateMachine", None)

    def update(self):
        checkExit(self.gStateMachine, self.score)

        if "\n" in keysPressed:
            self.gStateMachine.change(
                "serve",
                {
                    "level": self.level + 1,
                    "paddle": Paddle.Paddle(),
                    "bricks": BricksMaker.createBricks(self.level + 1),
                    "health": self.health,
                    "score": self.score,
                    "gStateMachine": self.gStateMachine,
                },
            )

    def render(self):
        if self.victory and self.level == LAST_LEVEL:
            window.draw(GAME_WON, 0, (WINDOW_WIDTH - 69) // 2, (WINDOW_HEIGHT - 6) // 2)
        elif not self.victory:
            window.draw(
                GAME_OVER, 0, (WINDOW_WIDTH - 71) // 2, (WINDOW_HEIGHT - 6) // 2
            )
        else:
            _message = f"Level {self.level} complete! Press Enter to serve!"
            window.draw(
                _message,
                0,
                (WINDOW_WIDTH - len(_message)) // 2,
                (WINDOW_HEIGHT - 1) // 2,
            )
        window.draw("{BREAKOUT}", 0, (WINDOW_WIDTH - 10) // 2, 0)
        renderScore(self.score)

        if not self.victory or self.victory and self.level == LAST_LEVEL:
            window.display()
            sys.exit()
