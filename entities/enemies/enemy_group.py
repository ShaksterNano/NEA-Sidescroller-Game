import math
import random
from .melee_enemy import *
from .shoot_enemy import *


class EnemyGroup:
    def __init__(self, game):
        self._game = game
        random.seed(self._game.get_seed())

        self._enemy_sprites = pygame.sprite.Group()
        self._max_enemies = g_max_enemies
        self._enemy_count = 0
        self._cooldown = 0
        self._max_spawn_cooldown = 500
        self._min_spawn_cooldown = 60
        self._min_cooldown_time = 1000
        self._melee_chance = g_enemy_melee_chance

    def update(self):
        self.add_enemy()
        self._enemy_sprites.update()
        self.remove_enemy()

    def add_enemy(self):
        if self._enemy_count < self._max_enemies:
            chance = random.randint(1, g_enemy_spawn_chance)
            melee_chance = random.random()
            if self._cooldown > 0:
                self._cooldown -= 1
            elif chance == 1:
                if melee_chance <= self._melee_chance:
                    self._enemy_sprites.add(MeleeEnemy(self._game, self._game.get_display_width() - 1,
                                                       self._game.get_display_height() - self._game.get_terrain().get_map()[
                                                           self._game.get_terrain().get_terrain_res() - 1], g_red))
                else:
                    self._enemy_sprites.add(ShootEnemy(self._game, self._game.get_display_width() - 1,
                                                       self._game.get_display_height() - self._game.get_terrain().get_map()[
                                                           self._game.get_terrain().get_terrain_res() - 1], g_blue))
                self._enemy_count += 1
                self._cooldown = (self._max_spawn_cooldown - self._min_spawn_cooldown) * math.e ** (
                            -1 / self._min_cooldown_time * self._game.get_player().get_offset()) + self._min_spawn_cooldown

    def remove_enemy(self):
        for enemy in self._enemy_sprites:
            if enemy.get_health() <= 0:
                enemy.kill()
                self._enemy_count -= 1
                self._game.increment_kills(1)
            if enemy.rect.right < 0:
                enemy.kill()
                self._enemy_count -= 1

    def draw_health_bars(self, display):
        for enemy in self._enemy_sprites:
            enemy.get_health_bar().draw(display)

    # Accessors
    def get_enemy_sprites(self):
        return self._enemy_sprites

    def set_enemy_sprites(self, enemies):
        self._enemy_sprites = enemies
