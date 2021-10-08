import random
from .coin import *
from .health_pack import *


class CollectableGroup:
    def __init__(self, game):
        self._game = game
        random.seed(self._game.get_seed() + 1)

        self._collectable_sprites = pygame.sprite.Group()
        first_coin_pos = random.randint(self._game.get_player().get_list_offset(),
                                        self._game.get_terrain().get_terrain_res())
        first_health_pos = random.randint(self._game.get_player().get_list_offset(),
                                          self._game.get_terrain().get_terrain_res())
        self.add_collectables(Coin, g_height_width * first_coin_pos,
                              self._game.get_display_height() - self._game.get_terrain().get_map()[
                                  first_coin_pos] - g_coin_ground_distance, 1, g_gold, 3, 50)
        self.add_collectables(HealthPack, g_height_width * first_health_pos,
                              self._game.get_display_height() - self._game.get_terrain().get_map()[
                                  first_health_pos] - g_health_pack_ground_distance, 1, g_green, 1, 0)
        self._coin_min_distance_between = self._game.get_display_width() / 8
        self._coin_max_distance_between = self._game.get_display_width() * (5 / 8)
        self._health_min_distance_between = self._game.get_display_width() * (7 / 8)
        self._health_max_distance_between = self._game.get_display_width() * 20

    def update(self):
        self.place_collectables()
        self._collectable_sprites.update()
        self.collect()
        self.remove_collectable()

    def place_collectables(self):
        furthest_coin_x = 0
        furthest_health_x = 0
        for furthest in self._collectable_sprites:
            if type(furthest) is Coin:
                if furthest.rect.right > furthest_coin_x:
                    furthest_coin_x = furthest.rect.right
            elif type(furthest) is HealthPack:
                if furthest.rect.right > furthest_health_x:
                    furthest_health_x = furthest.rect.right
        next_coin_pos = furthest_coin_x + random.randint(self._coin_min_distance_between,
                                                         self._coin_max_distance_between)
        next_health_pos = furthest_health_x + random.randint(self._health_min_distance_between,
                                                             self._health_max_distance_between)
        if next_coin_pos <= self._game.get_display_width():
            self.add_collectables(Coin, self._game.get_display_width(),
                                  self._game.get_display_height() - self._game.get_terrain().get_map()[
                                      self._game.get_terrain().get_terrain_res() - 1] - g_coin_ground_distance, 1,
                                  g_gold, 3, 50)
        if next_health_pos <= self._game.get_display_width():
            self.add_collectables(HealthPack, self._game.get_display_width(),
                                  self._game.get_display_height() - self._game.get_terrain().get_map()[
                                      self._game.get_terrain().get_terrain_res() - 1] - g_health_pack_ground_distance,
                                  1,
                                  g_green, 1, 0)

    def add_collectables(self, collectable, x, y, value, colour, quantity, distance):
        for count in range(quantity):
            self._collectable_sprites.add(collectable(self._game, x + count * distance, y, value, colour))

    def collect(self):
        collect = pygame.sprite.spritecollide(self._game.get_player(), self._collectable_sprites, True)
        for collectable in collect:
            collectable.collect()

    def remove_collectable(self):
        for coin in self._collectable_sprites:
            if coin.rect.right < 0:
                coin.kill()

    def draw_collectable(self, display):
        self._collectable_sprites.draw(display)

