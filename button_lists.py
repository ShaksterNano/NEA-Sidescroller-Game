from button import *


def main_menu_buttons(buttons, display_width, display_height, game_loop, upgrades_menu, quit_game):
    buttons.clear()
    buttons.append(Button(display_width / 2 - g_button_width / 2, 300, g_button_width, g_button_height, g_dark_green, g_green, "Play", game_loop))
    buttons.append(Button(display_width / 2 - g_button_width / 2, 400, g_button_width, g_button_height, g_dark_green, g_green, "Upgrades", upgrades_menu))
    buttons.append(Button(display_width / 2 - g_button_width / 2, 500, g_button_width, g_button_height, g_dark_green, g_green, "Quit", quit_game))
    return buttons


def upgrade_main_menu_buttons(buttons, display_width, display_height, upgrade, return_to_menu, upgrades):
    buttons.clear()
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 300, g_wide_button_width, g_button_height, g_dark_green, g_green, "Upgrade damage: ", upgrade, "extra_damage", str(upgrades["extra_damage"][0])))
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 400, g_wide_button_width, g_button_height, g_dark_green, g_green, "Upgrade health: ", upgrade, "extra_health", str(upgrades["extra_health"][0])))
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 500, g_wide_button_width, g_button_height, g_dark_green, g_green, "Upgrade jumps: ", upgrade, "extra_jumps", str(upgrades["extra_jumps"][0])))
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 600, g_wide_button_width, g_button_height, g_dark_green, g_green, "Return to menu", return_to_menu))
    return buttons


def pause_buttons(buttons, display_width, display_height, unpause, return_to_menu, in_game_quit):
    buttons.clear()
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 300, g_wide_button_width, g_button_height, g_dark_green, g_green, "Resume", unpause))
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 400, g_wide_button_width, g_button_height, g_dark_green, g_green, "Return to menu", return_to_menu))
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 500, g_wide_button_width, g_button_height, g_dark_green, g_green, "Quit", in_game_quit))
    return buttons


def game_over_buttons(buttons, display_width, display_height, play_again, return_to_menu, in_game_quit):
    buttons.clear()
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 300, g_wide_button_width, g_button_height, g_dark_green, g_green, "Play again", play_again))
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 400, g_wide_button_width, g_button_height, g_dark_green, g_green, "Return to menu", return_to_menu))
    buttons.append(Button(display_width / 2 - g_wide_button_width / 2, 500, g_wide_button_width, g_button_height, g_dark_green, g_green, "Quit", in_game_quit))
    return buttons
