from .collectable import *


class HealthPack(Collectable):
    def __init__(self, game, x, y, value, colour):
        super().__init__(game, x, y, value, colour)

    def collect(self):
        self._game.increase_health(self._value)
