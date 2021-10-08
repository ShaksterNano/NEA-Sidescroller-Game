from .perlin_noise_2d import *
from .shift import *
from .height import *


class Terrain:
    def __init__(self, game):
        self._game = game
        self._y = g_y
        self._octaves = g_octaves
        self._seed = g_seed
        self._terrain_res = int(game.get_display_width() / g_height_width)
        self._map = [g_terrain_height] * self._terrain_res
        self._terrain_sprites = pygame.sprite.Group()

        # Generates the starting heightmap values, before any scrolling begins
        noise_x = 0
        for count in range(len(self._map)):
            amp = 1
            for oct_count in range(1, self._octaves + 1):
                self._map[count] += amp * noise(oct_count * noise_x, oct_count * self._y, self._seed)
                amp *= 0.5
            self._map[count] *= g_noise_multiplier
            noise_x += g_map_length / self._terrain_res

        height_pos = 0
        for count in range(len(self._map)):
            self._terrain_sprites.add(Height(self._game, height_pos, self._map[count]))
            height_pos += g_height_width

    def update(self, offset, offset_change):  # Generates heightmap values in the direction specified and adds them to the heightmap
        if offset_change != 0:
            for position in range(abs(offset_change) - 1, -1, -1):
                amp = 1
                noise_x = g_map_length / self._terrain_res
                height = g_terrain_height
                right = False
                if offset_change > 0:  # If scrolling right
                    for oct_count in range(1, self._octaves + 1):
                        height += amp * noise(oct_count * (g_map_length + (offset - position) * noise_x), oct_count * self._y, self._seed)
                        amp *= 0.5
                    right = True
                elif offset_change < 0:  # If scrolling left
                    for oct_count in range(1, self._octaves + 1):
                        height += amp * noise(oct_count * (offset + position) * noise_x, oct_count * self._y, self._seed)
                        amp *= 0.5
                    right = False
                self._map = shift(self._map, right, height * g_noise_multiplier)

            self._terrain_sprites.empty()
            height_pos = 0
            for count in range(len(self._map)):
                self._terrain_sprites.add(Height(self._game, height_pos, self._map[count]))
                height_pos += g_height_width

    # Accessors
    def get_terrain_res(self):
        return self._terrain_res

    def get_map(self):
        return self._map

    def set_map(self, map):
        self._map = map

    def get_terrain_sprites(self):
        return self._terrain_sprites

    def set_terrain_sprites(self, terrain):
        self._terrain_sprites = terrain
