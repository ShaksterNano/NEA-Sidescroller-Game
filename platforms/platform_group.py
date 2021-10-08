import random
from .platform import *


class PlatformGroup:
    def __init__(self, game):
        self._game = game
        random.seed(self._game.get_seed())

        self._platform_sprites = pygame.sprite.Group()
        first_plat_pos = random.randint(self._game.get_player().get_list_offset(), self._game.get_terrain().get_terrain_res())
        self._platform_sprites.add(Platform(g_height_width * first_plat_pos, self._game.get_display_height() - self._game.get_terrain().get_map()[first_plat_pos] - g_platform_ground_distance))
        self._max_platforms = g_max_platforms
        self._platform_count = 1
        self._min_distance_between = self._game.get_display_width() / 4
        self._max_distance_between = self._game.get_display_width() * (3 / 4)

    def update(self, offset_change):
        self.add_platform()
        self._platform_sprites.update(offset_change)
        self.remove_platform()

    def add_platform(self):
        furthest_x = 0
        if self._platform_count < self._max_platforms:
            for furthest in self._platform_sprites:
                if furthest.rect.right > furthest_x:
                    furthest_x = furthest.rect.right
            next_plat_pos = furthest_x + random.randint(self._min_distance_between, self._max_distance_between)
            if next_plat_pos <= self._game.get_display_width():
                self._platform_sprites.add(Platform(self._game.get_display_width(), self._game.get_display_height() - self._game.get_terrain().get_map()[self._game.get_terrain().get_terrain_res() - 1] - g_platform_ground_distance))
                self._platform_count += 1

    def remove_platform(self):
        for platform in self._platform_sprites:
            if platform.rect.right < 0:
                platform.kill()
                self._platform_count -= 1

    # Accessors
    def get_platform_sprites(self):
        return self._platform_sprites

    def set_platform_sprites(self, platforms):
        self._platform_sprites = platforms
