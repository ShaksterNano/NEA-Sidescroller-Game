import pygame
from text import *
from settings import *

vector = pygame.math.Vector2


class Button:
    def __init__(self, x, y, width, height, inactive_colour, hover_colour, text, action=None, upgrade=None, value=""):
        self._pos = vector(x, y)
        self._width = width
        self._height = height
        self._inactive_colour = inactive_colour
        self._hover_colour = hover_colour
        self._colour = inactive_colour
        self._original_text = text
        self._text = self._original_text + value
        self._mouse_down_before = False
        self._mouse_down_after = False
        self.action = action
        self._upgrade = upgrade

        self._font = pygame.font.SysFont("comicsansms", 20)
        self._textSurf, self._textRect = text_objects(self._text, self._font, g_black)
        self._textRect.center = ((self._pos.x + (self._width / 2)), (self._pos.y + (self._height / 2)))

    def update(self, upgrades=None):
        click = pygame.mouse.get_pressed(3)
        mouse_pos = pygame.mouse.get_pos()
        self._mouse_down_before = self._mouse_down_after
        self._mouse_down_after = click[0]
        if self._upgrade is not None:
            self._text = self._original_text + str(upgrades[self._upgrade][0])
        if self._pos.x + self._width > mouse_pos[0] > self._pos.x and self._pos.y + self._height > mouse_pos[1] > self._pos.y:
            self._colour = self._hover_colour
            if not self._mouse_down_before and self._mouse_down_after and self.action is not None:
                if self._upgrade is None:
                    self.action()
                else:
                    self.action(self._upgrade)
        else:
            self._colour = self._inactive_colour

        self._textSurf, self._textRect = text_objects(self._text, self._font, g_black)
        self._textRect.center = ((self._pos.x + (self._width / 2)), (self._pos.y + (self._height / 2)))

    def draw(self, display):
        pygame.draw.rect(display, self._colour, (int(self._pos.x), int(self._pos.y), self._width, self._height))
        display.blit(self._textSurf, self._textRect)
