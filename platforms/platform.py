import pygame
from settings import *

vector = pygame.math.Vector2


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self._pos = vector(x, y)
        self._width = g_platform_width
        self._height = g_platform_height
        self._colour = g_platform_colour

        self.image = pygame.Surface((self._width, self._height))
        self.image.fill(self._colour)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self._pos

    def update(self, offset_change):
        self._pos.x += -1 * offset_change * g_height_width
        self.rect.left = self._pos.x

