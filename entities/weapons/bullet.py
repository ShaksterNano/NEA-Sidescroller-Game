import pygame
import math
import random
from settings import *

vector = pygame.math.Vector2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, player_bullet, damage, inaccuracy, colour, x1, y1, x2, y2):
        pygame.sprite.Sprite.__init__(self)
        self._game = game

        self._side_length = g_bullet_side_length
        self._colour = colour
        self._pos = vector(x1, y1)
        self._angle = math.atan2(y1 - y2, x2 - x1) + random.uniform(-1 * inaccuracy, inaccuracy)
        self._vel = g_bullet_speed * vector(math.cos(self._angle), -1 * math.sin(self._angle))
        self._player_bullet = player_bullet
        self._damage = damage

        self.image = pygame.Surface((self._side_length, self._side_length))
        self.image.fill(self._colour)
        self.rect = self.image.get_rect()
        self.rect.center = self._pos

    def update(self):
        player_offset_change = self._game.get_player().get_offset_change()
        self._pos.x += -1 * player_offset_change * g_height_width
        self._pos += self._vel
        self.rect.center = self._pos

    def get_player_bullet(self):
        return self._player_bullet

    def set_player_bullet(self, player_bullet):
        self._player_bullet = player_bullet

    def get_damage(self):
        return self._damage

    def set_damage(self, damage):
        self._damage = damage
