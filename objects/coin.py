from .collectable import *


class Coin(Collectable):
    def __init__(self, game, x, y, value, colour):
        super().__init__(game, x, y, value, colour)

    def collect(self):
        self._game.increment_coins(self._value)
