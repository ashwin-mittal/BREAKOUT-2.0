from Util import Timer
from constants import WINDOW_WIDTH


class StateMachine:
    def __init__(self, states):
        self.states = states or {}

        class Empty:
            def render(self):
                pass

            def update(self):
                pass

            def enter(self):
                pass

            def exit(self):
                pass

        self.current = Empty()
        self.timer = Timer()
        self.x = WINDOW_WIDTH

    def change(self, stateName, enterParams):
        self.current.exit()
        self.current = self.states[stateName]()
        self.current.enter(enterParams)

    def update(self):
        # self.x -= 0.25
        # if self.x <= -66:
        #     self.x = WINDOW_WIDTH
        # Background rendering
        # window.draw(
        #     BACKGROUND,
        #     0,
        #     self.x,
        #     (WINDOW_HEIGHT - 14) // 2,
        # )
        self.timer.render()
        self.current.update()

    def render(self):
        self.current.render()

    def getTime(self):
        return self.timer.getTime()
