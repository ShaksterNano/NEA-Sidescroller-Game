from .enemy import *


class MeleeEnemy(Enemy):
    def __init__(self, game, x, y, colour):
        super().__init__(game, x, y, colour)

        self._melee_damage = g_enemy_melee_damage
        self._melee_range = vector(g_enemy_melee_x_range, g_enemy_melee_y_range)
        self._melee_cooldown = g_enemy_melee_cooldown

    def horizontal_movement(self):
        self._attack_range = self._melee_range.x
        super().horizontal_movement()
        self.melee_attack()

    def melee_attack(self):
        if self._melee_cooldown_remaining == 0:
            player = self._game.get_player()
            if 0 <= self._facing * (player.get_pos_x() - self._pos.x) <= self._melee_range.x:
                if abs(player.get_pos_y() - self._pos.y) <= self._melee_range.y:
                    player.take_damage(self._melee_damage)
                    self._melee_cooldown_remaining = self._melee_cooldown
