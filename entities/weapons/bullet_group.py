from .bullet import *


class BulletGroup:
    def __init__(self, game):
        self._game = game
        self._bullet_sprites = pygame.sprite.Group()

    def update(self):
        self._bullet_sprites.update()
        self.bullet_collide()
        self.offscreen_bullet()

    def add_bullet(self, player_bullet, damage, inaccuracy, colour, x1, y1, x2, y2):
        self._bullet_sprites.add(Bullet(self._game, player_bullet, damage, inaccuracy, colour, x1, y1, x2, y2))

    def bullet_collide(self):
        for bullet in self._bullet_sprites:
            terrain_collide = pygame.sprite.spritecollide(bullet, self._game.get_terrain().get_terrain_sprites(), False)
            if bullet.get_player_bullet():
                enemy_collide = pygame.sprite.spritecollide(bullet, self._game.get_enemies().get_enemy_sprites(), False)
                if enemy_collide:
                    enemy_collide[0].take_damage(bullet.get_damage())
                    bullet.kill()
            else:
                player_collide = pygame.sprite.collide_rect(bullet, self._game.get_player())
                if player_collide:
                    self._game.get_player().take_damage(bullet.get_damage())
                    bullet.kill()
            if terrain_collide:
                bullet.kill()

    def offscreen_bullet(self):
        for bullet in self._bullet_sprites:
            if bullet.rect.right < 0 or bullet.rect.left > self._game.get_display_width() or bullet.rect.bottom < 0 or bullet.rect.top > self._game.get_display_height():
                bullet.kill()

    def draw_bullets(self, display):
        self._bullet_sprites.draw(display)

    def get_bullet_sprites(self):
        return self._bullet_sprites
