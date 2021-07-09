# BricksMaker Class.
import random

import constants
from Brick import Brick


class BricksMaker:
    # Creates a table of Bricks to
    # be returned to the main game.
    @staticmethod
    def createBricks(level):
        bricks = []

        # Some approximations.
        numRows = constants.WINDOW_HEIGHT // 8
        numCols = constants.WINDOW_WIDTH // 8
        numCols = numCols + (numCols % 2 == 0)

        # numRows = 1
        # numCols = 1

        highestColor = len(constants.COLORS)

        for y in range(numRows):
            # Some randomization.
            skipPattern = random.randint(0, 1)
            skipFlag = random.randint(0, 1)

            alternateFlag = random.randint(0, 1)
            alternatePattern = random.randint(0, 1)

            alternateColor1 = random.choice(range(1, highestColor))
            alternateColor2 = random.choice(range(1, highestColor))

            solidColor = random.choice(range(1, highestColor))

            for x in range(numCols):
                if skipPattern and skipFlag:
                    skipFlag = not skipFlag
                    continue
                else:
                    skipFlag = not skipFlag

                # x-coordinate and
                # y-coordinate.
                b = Brick(
                    x * 7 + (constants.WINDOW_WIDTH - numCols * 7) // 2,
                    (y + 3) * 3 + 1,
                )

                if level == constants.LAST_LEVEL and b.type:
                    continue

                if alternatePattern and alternateFlag:
                    b.color = alternateColor1
                    alternateFlag = not alternateFlag
                else:
                    b.color = alternateColor2
                    alternateFlag = not alternateFlag

                if not alternatePattern:
                    b.color = solidColor

                bricks.append(b)

        # A list of Bricks returned
        # to the main game.
        return bricks
