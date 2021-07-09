# Powerups.
# 0: Increase paddle size.
# 1: Decrease paddle size.
# 2: Multiple balls.
# 3: Fast ball.
# 4: Through ball.
# 5: Paddle grab.
# 6: Shooting paddle.
# 7: Fire ball.


class PaddleGrab:
    @staticmethod
    def add(paddle, balls, powerup, start_time):
        paddle.isGrab += 1

    @staticmethod
    def remove(paddle, balls, powerup):
        paddle.isGrab -= 1
