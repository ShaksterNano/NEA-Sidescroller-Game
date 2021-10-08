import pygame
import math
from settings import *

vector = pygame.math.Vector2


class Height(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)

        self._game = game
        self._pos = vector(x, y)
        self.image = pygame.Surface((g_height_width, math.ceil(self._pos.y)))
        self.image.fill(g_grass)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self._pos.x, self._game.get_display_height())
