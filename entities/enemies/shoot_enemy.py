from .enemy import *


class ShootEnemy(Enemy):
    def __init__(self, game, x, y, colour):
        super().__init__(game, x, y, colour)

        self._bullet_damage = g_enemy_bullet_damage
        self._inaccuracy = g_enemy_inaccuracy
        self._shoot_range = vector(g_enemy_shoot_range, 0)
        self._back_off_range = g_enemy_back_off_range
        self._shoot_cooldown = g_enemy_shoot_cooldown

    def horizontal_movement(self):
        self._attack_range = self._shoot_range.x
        super().horizontal_movement()

        if self._back_off_range >= self._player_distance >= 0:
            self._pos.x -= self._vel.x
            self._facing = -1
        elif -1 * self._back_off_range <= self._player_distance <= 0:
            self._pos.x += self._vel.x
            self._facing = 1

        if abs(self._player_distance) <= self._shoot_range.x:
            self.shoot(g_black, self._game.get_player().get_pos_x(), self._game.get_player().get_pos_y() - g_player_height / 2)

    def shoot(self, colour, x, y):
        if self._shoot_cooldown_remaining == 0:
            self._game.add_bullet(False, self._bullet_damage, self._inaccuracy, colour, self.rect.centerx, self.rect.centery, x, y)
            self._shoot_cooldown_remaining = self._shoot_cooldown
