import pygame
import math
from settings import *

vector = pygame.math.Vector2


class Collectable(pygame.sprite.Sprite):
    def __init__(self, game, x, y, value, colour):
        pygame.sprite.Sprite.__init__(self)

        self._game = game
        self._pos = vector(x, y)
        self._value = value
        self._colour = colour
        self._side_length = g_coin_side_length * (math.log(self._value) + 1)

        self.image = pygame.Surface((self._side_length, self._side_length))
        self.image.fill(self._colour)
        self.rect = self.image.get_rect()
        self.rect.center = self._pos

    def update(self):
        player_offset_change = self._game.get_player().get_offset_change()
        self._pos.x += -1 * player_offset_change * g_height_width
        self.rect.center = self._pos
