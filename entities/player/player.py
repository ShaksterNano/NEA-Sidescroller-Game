from ..entity import *


class Player(Entity):
    def __init__(self, game):
        super().__init__(game)

        self._width = g_player_width
        self._height = g_player_height
        self._colour = g_black

        self._offset = 0
        self._offset_change = 0

        self._list_offset = int(self._game.get_terrain().get_terrain_res() / 2)

        self._pos = vector(self._list_offset * g_height_width,
                           self._game.get_display_height() - self._game.get_terrain().get_map()[self._list_offset])
        self._vel = vector(g_player_speed, 0)

        self._max_health = g_player_health
        self._health = self._max_health + self._game.get_upgrades()["extra_health"][0]
        self._health_bar = HealthBar(self._max_health, g_player_health_bar_width, g_player_health_bar_height, g_player_health_bar_x, self._game.get_display_height() - 80)

        self._melee_mode = True

        self._can_melee_attack = False
        self._melee_damage = g_player_melee_damage + self._game.get_upgrades()["extra_damage"][0]
        self._melee_range = vector(g_player_melee_x_range, g_player_melee_y_range)
        self._backwards_melee_range = g_player_backwards_melee_range
        self._melee_cooldown = g_player_melee_cooldown

        self._can_shoot = False
        self._bullet_damage = g_player_bullet_damage + self._game.get_upgrades()["extra_damage"][0]
        self._inaccuracy = g_player_inaccuracy
        self._shoot_cooldown = g_player_shoot_cooldown

        self._jumps += self._game.get_upgrades()["extra_jumps"][0]

        self.image = pygame.Surface((self._width, self._height))
        self.image.fill(self._colour)
        self.rect = self.image.get_rect()
        self.rect.centerx = self._pos.x
        self.rect.bottom = self._pos.y

    def update(self):
        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed(3)
        mouse_pos = pygame.mouse.get_pos()
        if keys[pygame.K_s]:
            self._can_drop_down = True
        if click[0]:
            self._can_melee_attack = True
            self._can_shoot = True

        if self._melee_mode:
            self._vel.x = g_player_melee_speed
        else:
            self._vel.x = g_player_speed

        self.horizontal_movement(keys)
        if self._pos.x < 30:
            self._pos.x = 30

        self._health_bar.update(self._health, g_player_health_bar_x, self._game.get_display_height() - 80)
        self.melee_attack()
        self.shoot(g_black, mouse_pos[0], mouse_pos[1])

        super().update()

        self._can_jump = False
        self._can_drop_down = False
        self._can_melee_attack = False
        self._can_shoot = False
        self._game.set_distance(int(self._offset / 10))

    def horizontal_movement(self, keys):
        self._offset_change = 0
        if keys[pygame.K_a]:
            self._facing = -1
            self._pos.x -= self._vel.x
        if keys[pygame.K_d]:
            self._facing = 1
            if self._pos.x == self._game.get_display_width() / 2:
                self._offset_change = int(self._vel.x / g_height_width)
            else:
                self._pos.x += self._vel.x
                if self._pos.x > self._game.get_display_width() / 2:
                    self._pos.x = self._game.get_display_width() / 2
        if keys[pygame.K_a] and keys[pygame.K_d]:
            self._offset_change = 0
        self._offset += self._offset_change

    def switch_attack_mode(self):
        self._melee_mode = not self._melee_mode

    def melee_attack(self):
        if self._melee_mode and self._melee_cooldown_remaining == 0 and self._can_melee_attack:
            for enemy in self._game.get_enemies().get_enemy_sprites():
                if 0 <= self._facing * (enemy.get_pos_x() - self._pos.x) <= self._melee_range.x or abs(enemy.get_pos_x() - self._pos.x) <= self._backwards_melee_range:
                    if abs(enemy.get_pos_y() - self._pos.y) <= self._melee_range.y:
                        enemy.take_damage(self._melee_damage)
                        self._melee_cooldown_remaining = self._melee_cooldown

    def shoot(self, colour, x, y):
        if not self._melee_mode and self._shoot_cooldown_remaining == 0 and self._can_shoot:
            self._game.add_bullet(True, self._bullet_damage, self._inaccuracy, colour, self.rect.centerx, self.rect.centery, x, y)
            self._shoot_cooldown_remaining = self._shoot_cooldown

    # Accessors
    def get_offset(self):
        return self._offset

    def set_offset(self, offset):
        self._offset = offset

    def get_offset_change(self):
        return self._offset_change

    def set_offset_change(self, offset_change):
        self._offset_change = offset_change

    def get_list_offset(self):
        return self._list_offset

    def get_melee_mode(self):
        return self._melee_mode

    def set_melee_mode(self, melee_mode):
        self._melee_mode = melee_mode
