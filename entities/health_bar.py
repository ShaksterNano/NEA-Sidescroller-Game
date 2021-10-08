import pygame
from settings import *

vector = pygame.math.Vector2


class HealthBar:
    def __init__(self, max_health, max_width, height, pos_x, pos_y):
        self._max_health = max_health
        self._max_width = max_width
        self._width = self._max_width
        self._height = height
        self._pos = vector(pos_x, pos_y)
        self._colour = g_green

    def update(self, health, x, y):
        self._pos = vector(x, y)
        self._width = int(self._max_width * (health / self._max_health))
        if self._width <= 0:
            self._width = 1
        if health <= 0.2 * self._max_health:
            self._colour = g_red
        elif health <= 0.5 * self._max_health:
            self._colour = g_orange

    def draw(self, display):
        pygame.draw.rect(display, self._colour, (int(self._pos.x), int(self._pos.y), self._width, self._height))
