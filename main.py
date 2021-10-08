import sys
import screeninfo
from file_handling import *
from button_lists import *
from terrain.terrain import *
from platforms.platform_group import *
from entities.player.player import *
from entities.enemies.enemy_group import *
from entities.weapons.bullet_group import *
from objects.collectable_group import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(g_caption)

        self._display_width = 0
        self._display_height = 0
        for m in screeninfo.get_monitors():
            self._display_width = m.width
            self._display_height = m.height

        self._display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self._clock = pygame.time.Clock()

        self._buttons = []
        self._game_running = False
        self._paused = False
        self._game_over = False
        self._secondary_menu_running = False

        self._seed = g_seed

        self._terrain = None
        self._player = None
        self._enemies = None
        self._bullets = None
        self._platforms = None
        self._collectables = None

        self._coins_collected = 0
        self._enemies_killed = 0
        self._distance_travelled = 0

        self._stats = {
            "coins": 0,
            "enemies_killed": 0,
            "distance_travelled": 0,
        }

        self._upgrades = {
            "extra_damage": [0, 0, 0],
            "extra_health": [0, 0, 0],
            "extra_jumps": [0, 0, 0]
        }

        self._play_again = False

    def check_events(self):  # Checks Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the close window button is pressed
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self._player.switch_attack_mode()
                if event.key == pygame.K_SPACE:
                    self._player.set_can_jump(True)
                if event.key == pygame.K_ESCAPE:
                    self._paused = not self._paused

    def menu(self):
        menu_running = True
        self._buttons = main_menu_buttons(self._buttons, self._display_width, self._display_height, self.game_loop, self.upgrades_menu, quit_game)
        font = pygame.font.SysFont("comicsansms", 115)
        while menu_running:
            self._stats = file_load("stats", self._stats)
            self._upgrades = array_file_load("upgrades", self._upgrades)
            self._display.fill(g_white)
            self.check_events()
            self.update_buttons()
            self.draw_buttons()
            message_display(self._display, self._display_width / 2, 100, "Sidescroller", font, g_black)
            self.update_display()
            if self._play_again:
                self.game_loop()

    def upgrades_menu(self):
        self._secondary_menu_running = True
        self._buttons = upgrade_main_menu_buttons(self._buttons, self._display_width, self._display_height, self.upgrade_stat, self.return_to_menu,
                                                  self._upgrades)
        font = pygame.font.SysFont("comicsansms", 115)
        small_font = font = pygame.font.SysFont("comicsansms", 30)
        while self._secondary_menu_running:
            self._display.fill(g_white)
            self.check_events()
            self.update_buttons(self._upgrades)
            self.draw_buttons()
            message_display(self._display, self._display_width / 2, 100, "Upgrades", font, g_black)
            message_display(self._display, self._display_width / 10, 100, "Coins: " + str(self._stats["coins"]), font, g_black)
            self.update_display()
            file_write("stats", self._stats)
            array_file_write("upgrades", self._upgrades)

    def update_buttons(self, upgrades=None):
        for button in self._buttons:
            button.update(upgrades)

    def draw_buttons(self):
        for button in self._buttons:
            button.draw(self._display)

    def upgrade_stat(self, upgrade):
        if self._stats["coins"] >= self._upgrades[upgrade][1]:
            if self._upgrades[upgrade][0] < self._upgrades[upgrade][2]:
                self._stats["coins"] -= self._upgrades[upgrade][1]
                self._upgrades[upgrade][0] += 1

    def init_game(self):
        self._coins_collected = 0
        self._enemies_killed = 0
        self._distance_travelled = 0

        self._terrain = Terrain(self)
        self._player = Player(self)
        self._enemies = EnemyGroup(self)
        self._bullets = BulletGroup(self)
        self._platforms = PlatformGroup(self)
        self._collectables = CollectableGroup(self)

    def game_loop(self):  # Main game loop
        self._play_again = False
        self._game_running = True
        self._paused = False
        self.init_game()
        while self._game_running:
            self.check_events()
            if self._paused:
                self.pause()
            self.game_update()
            self.game_draw()
            self.update_display()
            if self._player.get_health() == 0:
                self.game_over()

    def game_update(self):  # Updates variable values
        self._bullets.update()
        self._enemies.update()
        self._player.update()
        self._terrain.update(self._player.get_offset(), self._player.get_offset_change())
        self._platforms.update(self._player.get_offset_change())
        self._collectables.update()

    def game_draw(self):  # Calls all draw methods and updates the display
        self._display.fill(g_sky)

        self._bullets.draw_bullets(self._display)
        self._display.blit(self._player.image, self._player.rect)
        self._enemies.get_enemy_sprites().draw(self._display)

        self._terrain.get_terrain_sprites().draw(self._display)
        self._collectables.draw_collectable(self._display)
        self._platforms.get_platform_sprites().draw(self._display)

        if self._player.get_health() > 0:
            self._player.get_health_bar().draw(self._display)
        self._enemies.draw_health_bars(self._display)

        self.draw_hud()

    def draw_hud(self):
        font = pygame.font.SysFont("comicsansms", 30)
        message_display(self._display, self._display_width / 10, 100, "Coins collected: " + str(self._coins_collected), font, g_black)
        message_display(self._display, self._display_width / 10, 200, "Enemies killed: " + str(self._enemies_killed), font, g_black)
        message_display(self._display, self._display_width / 10, 300, "Distance travelled: " + str(self._distance_travelled), font, g_black)
        if self._player.get_melee_mode():
            pygame.draw.rect(self._display, g_red, (50, 869, 50, 50))
        else:
            pygame.draw.rect(self._display, g_blue, (50, 869, 50, 50))

    def pause(self):
        self._buttons = pause_buttons(self._buttons, self._display_width, self._display_height, self.unpause, self.in_game_return_to_menu, self.in_game_quit)
        font = pygame.font.SysFont("comicsansms", 115)
        message_display(self._display, self._display_width / 2, 100, "Paused", font, g_black)
        while self._paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._paused = not self._paused
            self.update_buttons()
            self.draw_buttons()
            self.update_display()

    def game_over(self):
        self._buttons = game_over_buttons(self._buttons, self._display_width, self._display_height, self.play_again, self.in_game_return_to_menu, self.in_game_quit)
        self._game_over = True
        font = pygame.font.SysFont("comicsansms", 115)
        message_display(self._display, self._display_width / 2, 100, "Game over", font, g_black)
        while self._game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
            self.update_buttons()
            self.draw_buttons()
            self.update_display()

    def unpause(self):
        self._paused = False

    def return_to_menu(self):
        self._secondary_menu_running = False
        self._buttons = main_menu_buttons(self._buttons, self._display_width, self._display_height, self.game_loop, self.upgrades_menu, quit_game)

    def in_game_return_to_menu(self):
        self._stats = save_stats("stats", self._stats, self._coins_collected, self._distance_travelled, self._enemies_killed)
        self.unpause()
        self._game_running = False
        self._game_over = False
        self._buttons = main_menu_buttons(self._buttons, self._display_width, self._display_height, self.game_loop, self.upgrades_menu, quit_game)

    def play_again(self):
        self._stats = save_stats("stats", self._stats, self._coins_collected, self._distance_travelled, self._enemies_killed)
        self.unpause()
        self._game_running = False
        self._game_over = False
        self._play_again = True

    def in_game_quit(self):
        self._stats = save_stats("stats", self._stats, self._coins_collected, self._distance_travelled, self._enemies_killed)
        quit_game()

    def update_display(self):
        pygame.display.update()
        self._clock.tick(g_max_fps)

    # Accessors
    def get_display_width(self):
        return self._display_width

    def get_display_height(self):
        return self._display_height

    def get_seed(self):
        return self._seed

    def get_terrain(self):
        return self._terrain

    def get_platform(self):
        return self._platforms

    def get_player(self):
        return self._player

    def get_enemies(self):
        return self._enemies

    def get_bullets(self):
        return self._bullets

    def add_bullet(self, player_bullet, damage, inaccuracy, colour, x1, y1, x2, y2):
        self._bullets.add_bullet(player_bullet, damage, inaccuracy, colour, x1, y1, x2, y2)

    def increment_coins(self, count):
        self._coins_collected += count

    def increment_kills(self, count):
        self._enemies_killed += count

    def set_distance(self, distance):
        self._distance_travelled = distance

    def increase_health(self, health):
        if self._player.get_health() < self._player.get_max_health():
            self._player.take_damage(-1 * health)
            if self._player.get_health() > self._player.get_max_health():
                self._player.set_health(self._player.get_max_health())

    def get_stats(self):
        return self._stats

    def get_upgrades(self):
        return self._upgrades


def quit_game():  # Quits the game
    pygame.quit()
    sys.exit()


game = Game()
game.menu()
