from .health_bar import *

vector = pygame.math.Vector2


class Entity(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self._game = game

        self._pos = vector(0, 0)
        self._vel = vector(0, 0)
        self._acc = vector(0, g_gravity)
        self._facing = 1

        self._max_health = 0
        self._health = self._max_health
        self._health_bar = HealthBar(self._max_health, 0, 0, 0, 0)

        self._melee_damage = 0
        self._melee_range = vector(0, 0)
        self._melee_cooldown_remaining = 0
        self._melee_cooldown_remaining = 0

        self._bullet_damage = 0
        self._shoot_cooldown = 0
        self._shoot_cooldown_remaining = 0

        self._current_terrain = []
        self._current_platform = []

        self._can_jump = False
        self._jump_speed = -1 * g_player_jump_speed
        self._can_drop_down = False
        self._jumps = 1
        self._jump_count = 0

    def update(self):
        self.collision()
        self.jump()

        # Update velocity and position variables
        self._vel.y += self._acc.y
        self._pos.y += self._vel.y + 0.5 * self._acc.y
        self.rect.bottomleft = self._pos

        if self._melee_cooldown_remaining > 0:
            self._melee_cooldown_remaining -= 1
        if self._shoot_cooldown_remaining > 0:
            self._shoot_cooldown_remaining -= 1

    def collision(self):
        self.rect.y += 1
        self._current_terrain = pygame.sprite.spritecollide(self, self._game.get_terrain().get_terrain_sprites(), False)
        self._current_platform = pygame.sprite.spritecollide(self, self._game.get_platform().get_platform_sprites(), False)
        self.rect.y -= 1
        current_height = self._game.get_display_height() * 100
        for height in self._current_terrain:
            if height.rect.top < current_height:
                current_height = height.rect.top

        if self._current_platform and self._vel.y > 0 and not self._can_drop_down:
            self._pos.y = self._current_platform[0].rect.top
            self._vel.y = 0
            self._jump_count = 0
        elif self._current_terrain:
            self._pos.y = current_height
            self._vel.y = 0
            self._jump_count = 0

    def jump(self):
        if (self._current_terrain or self._current_platform or self._jump_count < self._jumps) and self._can_jump:
            self._vel.y = self._jump_speed
            self._jump_count += 1

    def take_damage(self, damage):
        self._health -= damage

    # Accessors
    def get_pos_x(self):
        return self._pos.x

    def set_pos_x(self, pos_x):
        self._pos.x = pos_x

    def get_pos_y(self):
        return self._pos.y

    def set_pos_y(self, pos_y):
        self._pos.y = pos_y

    def get_vel_x(self):
        return self._vel.x

    def set_vel_x(self, vel_x):
        self._vel.x = vel_x

    def get_vel_y(self):
        return self._vel.y

    def set_vel_y(self, vel_y):
        self._vel.y = vel_y

    def get_gravity(self):
        return self._acc.y

    def set_gravity(self, gravity):
        self._acc.y = gravity

    def get_max_health(self):
        return self._max_health

    def set_max_health(self, max_health):
        self._max_health = max_health

    def get_health(self):
        return self._health

    def set_health(self, health):
        self._health = health

    def get_health_bar(self):
        return self._health_bar

    def set_health_bar(self, health_bar):
        self._health_bar = health_bar

    def get_can_jump(self):
        return self._can_jump

    def set_can_jump(self, can_jump):
        self._can_jump = can_jump
