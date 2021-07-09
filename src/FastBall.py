# CODE.
# Powerups.
# 0: Increase paddle size.
# 1: Decrease paddle size.
# 2: Multiple balls.
# 3: Fast ball.
# 4: Through ball.
# 5: Paddle grab.
# 6: Shooting paddle.
# 7: Fire ball.


class FastBall:
    @staticmethod
    def add(paddle, balls, powerup, start_time):
        for ball in balls:
            if abs(ball.dy) < 0.5:
                ball.dy *= 1.1
                ball.powerups.add(powerup)

    @staticmethod
    def remove(paddle, balls, powerup):
        for ball in balls:
            if powerup in ball.powerups:
                ball.powerups.remove(powerup)
                ball.dy /= 1.1
