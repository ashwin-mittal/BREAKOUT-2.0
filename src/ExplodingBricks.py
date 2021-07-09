# Powerups.
# 0: Increase paddle size.
# 1: Decrease paddle size.
# 2: Multiple balls.
# 3: Fast ball.
# 4: Through ball.
# 5: Paddle grab.
# 6: Shooting paddle.
# 7: Fire ball.


class ExplodingBricks:
    @staticmethod
    def explode(brick, bricks):
        score = 0
        for b in bricks:
            if b.inPlay:
                if (
                        abs(b.x - brick.x) <= brick.width
                        and abs(b.y - brick.y) <= brick.height
                ):
                    b.inPlay = False
                    score += b.color * 25
        return score
