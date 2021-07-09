# Powerups.
# 0: Increase paddle size.
# 1: Decrease paddle size.
# 2: Multiple balls.
# 3: Fast ball.
# 4: Through ball.
# 5: Paddle grab.
# 6: Shooting paddle.
# 7: Fire ball.


class ShootingPaddle:
    @staticmethod
    def add(paddle, balls, powerup, start_time):
        paddle.bulleted += 1
        paddle.bulletedTime = start_time

    @staticmethod
    def remove(paddle, balls, powerup):
        paddle.bulleted -= 1
