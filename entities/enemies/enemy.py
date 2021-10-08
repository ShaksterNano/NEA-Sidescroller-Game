from ..entity import *


class Enemy(Entity):
    def __init__(self, game, x, y, colour):
        super().__init__(game)

        self._width = g_player_width
        self._height = g_player_height
        self._colour = colour

        self._pos = vector(x, y)
        self._vel.x = g_enemy_speed
        self._player_detection_range = g_enemy_player_detection_range

        self._max_health = g_enemy_health
        self._health = self._max_health
        self._health_bar = HealthBar(self._max_health, g_enemy_health_bar_width, g_enemy_health_bar_height,
                                     self._pos.x + self._width / 2 - g_enemy_health_bar_width / 2,
                                     self._pos.y - self._height - g_height_above_enemy)

        self._attack_range = 0
        self._player_distance = 0

        self.image = pygame.Surface((self._width, self._height))
        self.image.fill(self._colour)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self._pos

    def update(self):
        player_offset_change = self._game.get_player().get_offset_change()

        self._pos.x += -1 * player_offset_change * g_height_width
        self.horizontal_movement()
        self._health_bar.update(self._health, self._pos.x + self._width / 2 - g_enemy_health_bar_width / 2,
                                self._pos.y - self._height - g_height_above_enemy)
        super().update()

    def locate_player(self):
        player = self._game.get_player()
        return player.get_pos_x() - self._pos.x

    def horizontal_movement(self):
        self._player_distance = self.locate_player()
        if self._player_detection_range > self._player_distance > self._attack_range:
            self._pos.x += self._vel.x
            self._facing = 1
        elif -1 * self._player_detection_range < self._player_distance < -1 * self._attack_range:
            self._pos.x -= self._vel.x
            self._facing = -1
        else:
            if self._player_distance * self._facing < 0:
                self._facing *= -1
