from Ball import Ball


# Powerups.
# 0: Increase paddle size.
# 1: Decrease paddle size.
# 2: Multiple balls.
# 3: Fast ball.
# 4: Through ball.
# 5: Paddle grab.
# 6: Shooting paddle.
# 7: Fire ball.


class MultipleBalls:
    @staticmethod
    def add(paddle, balls, powerup, start_time):
        for ball in balls[:]:
            newBall = Ball()
            newBall.x = ball.x
            newBall.y = ball.y
            newBall.dx = -ball.dx
            newBall.dy = ball.dy
            newBall.beforeGrabingdx = -ball.beforeGrabingdx
            newBall.beforeGrabingdy = ball.beforeGrabingdy
            newBall.powerups.add(powerup)
            balls.append(newBall)

    @staticmethod
    def remove(paddle, balls, powerup):
        for ball in balls[:]:
            if powerup in ball.powerups:
                if len(balls) == 1:
                    ball.powerups.remove(powerup)
                    break
                balls.remove(ball)
