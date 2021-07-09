from Ball import Ball
from BaseState import BaseState
from Util import checkExit, keysPressed, renderHealth, renderLevel, renderScore
from Window import window
from constants import LAST_LEVEL, WINDOW_WIDTH
from src.BossEnemy import BossEnemy


class ServeState(BaseState):
    def enter(self, params):
        self.level = params["level"]
        self.paddle = params["paddle"]
        self.bricks = params["bricks"]
        self.health = params["health"]
        self.score = params["score"]
        self.playTime = params.get("playTime", 0)
        self.gStateMachine = params["gStateMachine"]
        self.ball = Ball()
        self.lastTime = self.gStateMachine.getTime()

        if self.level == LAST_LEVEL:
            self.enemy = params.get("enemy", BossEnemy(self.paddle.skin))

    def update(self):
        currentTime = self.gStateMachine.getTime()
        deltaTime = currentTime - self.lastTime
        # self.playTime += deltaTime
        self.lastTime = currentTime

        checkExit(self.gStateMachine, self.score)

        self.paddle.update()

        if self.level == LAST_LEVEL:
            self.enemy.update(self.paddle, None, deltaTime)

        self.ball.x = self.paddle.x + ((self.paddle.width - self.ball.width) // 2)
        self.ball.y = self.paddle.y - self.ball.height

        # Change to the PlayState.
        if " " in keysPressed:
            self.gStateMachine.change(
                "play",
                {
                    "level": self.level,
                    "paddle": self.paddle,
                    "bricks": self.bricks,
                    "health": self.health,
                    "score": self.score,
                    "ball": self.ball,
                    "playTime": self.playTime,
                    "enemy": self.enemy if hasattr(self, "enemy") else None,
                    "gStateMachine": self.gStateMachine,
                },
            )

    def render(self):
        self.paddle.render()
        self.ball.render()

        if self.level == LAST_LEVEL:
            self.enemy.render()

        for brick in self.bricks:
            brick.render()

        renderScore(self.score)
        renderHealth(self.health)
        renderLevel(self.level)

        message = "PRESS SPACE TO SERVE!"
        window.draw(message, 0, (WINDOW_WIDTH - len(message)) // 2, 1)
