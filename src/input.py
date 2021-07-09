# TESTED.

import atexit
import sys
import termios
from select import select


class KBHit:
    """
    To take input.
    """

    def __init__(self):
        """Creates a KBHit object that you can call to do various keyboard things."""

        # Save the terminal settings.
        self.__fdd = sys.stdin.fileno()
        self.__new_term = termios.tcgetattr(self.__fdd)
        self.__old_term = termios.tcgetattr(self.__fdd)

        # New terminal setting unbuffered.
        self.__new_term[3] = self.__new_term[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.__fdd, termios.TCSAFLUSH, self.__new_term)

        # Support normal-terminal reset at exit.
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """Resets to normal terminal."""

        termios.tcsetattr(self.__fdd, termios.TCSAFLUSH, self.__old_term)

    @staticmethod
    def getch():
        """Returns a keyboard character after kbhit() has been called."""

        reader = sys.stdin.read(1)
        return reader.lower()

    @staticmethod
    def kbhit():
        """Returns True if keyboard character was hit, False otherwise."""
        return select([sys.stdin], [], [], 0)[0] != []

    @staticmethod
    def clear():
        """
        Clears the input buffer.
        """
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
