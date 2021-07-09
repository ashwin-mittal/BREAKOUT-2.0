# PlayState Class.
import random

from BaseState import BaseState
from DecreasePaddleSize import DecreasePaddleSize
from ExplodingBricks import ExplodingBricks
from FastBall import FastBall
from FireBall import FireBall
from IncreasePaddleSize import IncreasePaddleSize
from MultipleBalls import MultipleBalls
from PaddleGrab import PaddleGrab
from Powerup import Powerup
from ThruBall import ThruBall
from Util import (
    checkExit,
    keysPressed,
    renderEnemyHealth,
    renderHealth,
    renderLevel,
    renderPowerupTime,
    renderScore,
)
from constants import (
    FALLING_TIME,
    LAST_LEVEL,
    NUM_POWERUPS,
    POWERUP_TIME,
    WINDOW_HEIGHT,
)
from src.Bullet import Bullet
from src.ShootingPaddle import ShootingPaddle

POWERUPS = {
    0: IncreasePaddleSize.add,
    1: DecreasePaddleSize.add,
    2: MultipleBalls.add,
    3: FastBall.add,
    4: ThruBall.add,
    5: PaddleGrab.add,
    6: ShootingPaddle.add,
    7: FireBall.add,
}

REMOVE_POWERUPS = {
    0: IncreasePaddleSize.remove,
    1: DecreasePaddleSize.remove,
    2: MultipleBalls.remove,
    3: FastBall.remove,
    4: ThruBall.remove,
    5: PaddleGrab.remove,
    6: ShootingPaddle.remove,
    7: FireBall.remove,
}


class PlayState(BaseState):
    def enter(self, params):
        self.level = params["level"]
        self.paddle = params["paddle"]
        self.bricks = params["bricks"]
        self.health = params["health"]
        self.score = params["score"]
        self.balls = [params["ball"]]
        self.playTime = params["playTime"]
        self.powerups = []
        self.bullets = []
        self.gStateMachine = params["gStateMachine"]
        self.lastTime = self.gStateMachine.getTime()

        if self.level == LAST_LEVEL:
            self.enemy = params["enemy"]
            self.bombs = []

        for ball in self.balls:
            ball.dx = random.choice([-0.25, 0, 0.25])
            ball.dy = -0.25

    def update(self):
        currentTime = self.gStateMachine.getTime()
        deltaTime = currentTime - self.lastTime
        self.playTime += deltaTime
        self.lastTime = currentTime

        # If "q" is pressed, then exit.
        checkExit(self.gStateMachine, self.score)

        if self.checkVictory() or "\n" in keysPressed:
            self.gStateMachine.change(
                "game-over",
                {
                    "level": self.level,
                    "health": self.health,
                    "score": self.score,
                    "victory": True,
                    "gStateMachine": self.gStateMachine,
                },
            )

        if " " in keysPressed:
            for ball in self.balls:
                if ball.dx == 0 and ball.dy == 0:
                    ball.dx = ball.beforeGrabingdx
                    ball.dy = ball.beforeGrabingdy

        for bullet in self.bullets[:]:
            bullet.update()
            for brick in self.bricks:
                if brick.inPlay and bullet.collides(brick):
                    brick.change = 0
                    if brick.type:
                        self.score += brick.color * 25

                    # Trigger the brick's hit function,
                    # which removes it from play.
                    brick.hit()

                    self.bullets.remove(bullet)
                    break
                elif bullet.y <= 2:
                    self.bullets.remove(bullet)
                    break

        if self.paddle.bulleted:
            if "k" in keysPressed:
                self.bullets.append(
                    Bullet(self.paddle.x + 1, self.paddle.y - 1, self.paddle.skin)
                )
                self.bullets.append(
                    Bullet(
                        self.paddle.x + self.paddle.width - 3,
                        self.paddle.y - 1,
                        self.paddle.skin,
                    )
                )

        for powerup in self.powerups[:]:
            if powerup.inPlay:
                powerup.update(deltaTime)
                # Making the effect.
                if powerup.collides(self.paddle):
                    _time = self.gStateMachine.getTime()
                    POWERUPS[powerup.type](self.paddle, self.balls, powerup, _time)
                    powerup.inPlay = False
                    powerup.startTime = _time
                elif powerup.y >= WINDOW_HEIGHT:
                    self.powerups.remove(powerup)
            else:
                if self.gStateMachine.getTime() - powerup.startTime > POWERUP_TIME:
                    # Reversing the effect.
                    REMOVE_POWERUPS[powerup.type](self.paddle, self.balls, powerup)
                    self.powerups.remove(powerup)

        # Update positions
        # based on velocity.
        self.paddle.update(self.balls)

        if self.level == LAST_LEVEL:
            self.enemy.update(self.paddle, self.bombs, deltaTime)
            if self.enemy.health == 3 and self.enemy.spawns == 2:
                self.enemy.spawn(self.bricks)

            elif self.enemy.health == 2 and self.enemy.spawns == 1:
                self.enemy.spawn(self.bricks)

            for bomb in self.bombs[:]:
                bomb.update()
                if bomb.collides(self.paddle):
                    self.health -= 1
                    if self.health == 0:
                        self.gStateMachine.change(
                            "game-over",
                            {
                                "level": self.level,
                                "health": self.health,
                                "score": self.score,
                                "victory": False,
                                "gStateMachine": self.gStateMachine,
                            },
                        )
                    self.bombs.remove(bomb)
                elif bomb.y >= WINDOW_HEIGHT:
                    self.bombs.remove(bomb)

        for ball in self.balls[:]:
            ball.update(deltaTime)

            if (ball.dx or ball.dy) and ball.collides(self.paddle):
                if self.playTime >= FALLING_TIME:
                    for brick in self.bricks:
                        brick.y += 1
                        if brick.inPlay and self.paddle.y - brick.y == brick.height:
                            self.gStateMachine.change(
                                "game-over",
                                {
                                    "level": self.level,
                                    "health": self.health,
                                    "score": self.score,
                                    "victory": False,
                                    "gStateMachine": self.gStateMachine,
                                },
                            )

                # Raise ball above paddle in case
                # it goes below it, then reverse dy.
                ball.y = self.paddle.y - ball.height
                if self.paddle.isGrab:
                    ball.beforeGrabingdx = ball.dx
                    ball.beforeGrabingdy = -ball.dy
                    ball.dy = 0
                    ball.dx = 0
                else:
                    ball.dy = -ball.dy

                    # if we hit the paddle on its left side.
                    if ball.x < self.paddle.x + (self.paddle.width / 2):
                        ball.dx = -0.25 - (
                                (self.paddle.x + self.paddle.width / 2 - ball.x) / 32
                        )

                    # Else if we hit the paddle on its right side.
                    elif ball.x > self.paddle.x + (self.paddle.width / 2):
                        ball.dx = 0.25 + (
                                abs(self.paddle.x + self.paddle.width / 2 - ball.x) / 32
                        )

            if self.level == LAST_LEVEL and ball.collides(self.enemy):
                self.score += self.enemy.health * 100
                self.enemy.health -= 1

                if ball.x + 0.25 < self.enemy.x and ball.dx > 0:
                    ball.dx = -ball.dx
                    ball.x = self.enemy.x - ball.width
                    ball.y -= ball.dy
                elif ball.x + 0.75 > self.enemy.x + self.enemy.width and ball.dx < 0:
                    ball.dx = -ball.dx
                    ball.x = self.enemy.x + self.enemy.width
                    ball.y -= ball.dy
                elif ball.y < self.enemy.y:
                    ball.dy = -ball.dy
                    ball.y = self.enemy.y - ball.height
                    ball.x -= ball.dx
                else:
                    ball.dy = -ball.dy
                    ball.y = self.enemy.y + self.enemy.height
                    ball.x -= ball.dx

                if abs(ball.dy) < 0.5:
                    ball.dy *= 1.01

            for brick in self.bricks:
                brick.update(deltaTime)

                if brick.inPlay and ball.collides(brick):
                    brick.change = 0

                    if brick.type or ball.isThru:
                        self.score += brick.color * 25

                    # Trigger the brick's hit function,
                    # which removes it from play.
                    brick.hit()

                    # Random powerup generation
                    # and exploding bricks.
                    if (
                            not brick.inPlay or (ball.isFire and brick.type)
                    ) and self.level != LAST_LEVEL:
                        if (
                                random.choices((0, 1), weights=(0.75, 0.25))[0]
                                or ball.isFire
                        ):
                            self.score += ExplodingBricks.explode(brick, self.bricks)
                        if random.choices((0, 1), weights=(0.25, 0.75))[0]:
                            self.powerups.append(
                                Powerup(
                                    brick,
                                    random.choice(range(NUM_POWERUPS)),
                                    ball.dx,
                                    ball.dy,
                                )
                            )

                    if ball.isThru:
                        brick.inPlay = False
                        break

                    # Collision code for bricks.
                    # Collision in x-direction.
                    if ball.x + 0.25 < brick.x and ball.dx > 0:
                        ball.dx = -ball.dx
                        ball.x = brick.x - ball.width
                        ball.y -= ball.dy
                    elif ball.x + 0.75 > brick.x + brick.width and ball.dx < 0:
                        ball.dx = -ball.dx
                        ball.x = brick.x + brick.width
                        ball.y -= ball.dy
                    # Collision in y-direction.
                    elif ball.y < brick.y:
                        ball.dy = -ball.dy
                        ball.y = brick.y - ball.height
                        ball.x -= ball.dx
                    else:
                        ball.dy = -ball.dy
                        ball.y = brick.y + brick.height
                        ball.x -= ball.dx

                    # Increasing the velocity.
                    if abs(ball.dy) < 0.5:
                        ball.dy *= 1.01

                    break

            if ball.y >= WINDOW_HEIGHT:
                if len(self.balls) > 1:
                    self.balls.remove(ball)
                    continue

                self.health -= 1

                if self.health == 0:
                    self.gStateMachine.change(
                        "game-over",
                        {
                            "level": self.level,
                            "health": self.health,
                            "score": self.score,
                            "victory": False,
                            "gStateMachine": self.gStateMachine,
                        },
                    )
                else:
                    # Reverse the effects of the
                    # paddle-related powerups.
                    self.paddle.resetSize()
                    self.powerups.clear()
                    self.gStateMachine.change(
                        "serve",
                        {
                            "level": self.level,
                            "paddle": self.paddle,
                            "bricks": self.bricks,
                            "health": self.health,
                            "score": self.score,
                            "playTime": self.playTime,
                            "gStateMachine": self.gStateMachine,
                            "enemy": self.enemy if hasattr(self, "enemy") else None,
                        },
                    )

    def render(self):
        # Render bricks.
        for brick in self.bricks:
            brick.render()

        self.paddle.render()

        if self.level == LAST_LEVEL:
            self.enemy.render()

        for ball in self.balls:
            ball.render()

        for powerup in self.powerups:
            if powerup.inPlay:
                powerup.render()

        for bullet in self.bullets:
            bullet.render()

        renderScore(self.score)
        renderHealth(self.health)
        renderLevel(self.level)

        if self.level == LAST_LEVEL:
            renderEnemyHealth(self.enemy.health)
            for bomb in self.bombs:
                bomb.render()

        if self.paddle.bulleted:
            renderPowerupTime(
                POWERUP_TIME - self.gStateMachine.getTime() + self.paddle.bulletedTime
            )

    def checkVictory(self):
        for brick in self.bricks:
            if brick.inPlay and brick.type:
                return False

        if self.level != LAST_LEVEL:
            return True
        else:
            return self.enemy.health is 0
