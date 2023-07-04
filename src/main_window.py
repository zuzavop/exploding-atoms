"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21

Hlavní čast
Zajištění nastavení hry a přechodů do hry a nápovědy
"""

from os import environ

from setting import colors, window_width, window_height, field_size, font_path, background_path, game_title

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# because of hiding od pygame support

import pygame

import game_window
import help_window
import button


class Menu:
    def __init__(self):
        self.help_button = None
        self.big_display_button = None
        self.medium_display_button = None
        self.small_display_button = None
        self.against_person_button = None
        self.against_computer_button = None
        self.start_button = None

        pygame.init()

        # window size
        self.width = window_width
        self.height = window_height

        self.running = True
        self.computer_play = False

        # field size
        self.field_size = field_size

        # buttons colors
        self.size_colors = (colors["white"], colors["aqua"], colors["white"])
        self.size_colors_over = (colors["aqua"], colors["aqua"], colors["aqua"])
        self.player_color = (colors["white"], colors["aqua"])
        self.player_color_over = (colors["aqua"], colors["aqua"])

        # create window
        self.display: pygame.Surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # set font
        self.font = pygame.font.Font(font_path, self.display.get_width() // 20)

    def main_cycle(self):
        """ main cycle of menu """
        # background load
        bg = pygame.image.load(background_path)
        picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))

        # set title
        title = self.font.render(game_title, True, colors["white"])
        title_rect = title.get_rect()

        self.create_buttons()

        while self.running:
            # set background
            self.display.blit(picture, (0, 0))

            # show title
            title_rect.center = (self.display.get_width() // 2, 1.5 * self.display.get_height() // 8)
            self.display.blit(title, title_rect)

            self.start_button.show(self.display, self.display.get_width() // 2, 3.2 * self.display.get_height() // 8,
                                   self.display.get_width() // 6, self.display.get_height() // 9, colors["white"],
                                   colors["aqua"])

            if not self.running:
                break

            self.show_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:  # change of size
                    self.font = pygame.font.Font(font_path, self.display.get_width() // 20)
                    picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
                    title = self.font.render(game_title, True, colors["white"])
                    title_rect = title.get_rect()

            pygame.display.update()

    def create_buttons(self):
        self.start_button = button.Button("Start", colors["black"], colors["white"], self.start_game)

        self.against_computer_button = button.Button("Proti počítači", colors["black"], colors["black"],
                                                     self.set_computer_player, 42)
        self.against_person_button = button.Button("Proti protihráči", colors["black"], colors["black"],
                                                   self.set_person_player, 42)

        self.small_display_button = button.Button("4x4", colors["black"], colors["black"], self.set_small_field, 42)
        self.medium_display_button = button.Button("8x8", colors["black"], colors["black"], self.set_medium_field, 42)
        self.big_display_button = button.Button("12x12", colors["black"], colors["black"], self.set_big_field, 42)

        self.help_button = button.Button("Pravidla", colors["black"], colors["black"], self.show_help)

    def show_buttons(self):
        self.against_computer_button.show(self.display, 3 * self.display.get_width() // 8,
                                          5.4 * self.display.get_height() // 8, self.display.get_width() // 5,
                                          self.display.get_height() // 16, self.player_color[0],
                                          self.player_color_over[0])
        self.against_person_button.show(self.display, 5 * self.display.get_width() // 8,
                                        5.4 * self.display.get_height() // 8, self.display.get_width() // 5,
                                        self.display.get_height() // 16, self.player_color[1],
                                        self.player_color_over[1])
        self.small_display_button.show(self.display, 3 * self.display.get_width() // 8,
                                       4.5 * self.display.get_height() // 8,
                                       self.display.get_width() // 12, self.display.get_height() // 16,
                                       self.size_colors[0], self.size_colors_over[0])
        self.medium_display_button.show(self.display, self.display.get_width() // 2,
                                        4.5 * self.display.get_height() // 8,
                                        self.display.get_width() // 12, self.display.get_height() // 16,
                                        self.size_colors[1], self.size_colors_over[1])
        self.big_display_button.show(self.display, 5 * self.display.get_width() // 8,
                                     4.5 * self.display.get_height() // 8, self.display.get_width() // 12,
                                     self.display.get_height() // 16, self.size_colors[2], self.size_colors_over[2])
        self.help_button.show(self.display, self.display.get_width() // 2, 6.5 * (self.display.get_height() // 8),
                              self.display.get_width() // 6, self.display.get_height() // 9, colors["white"],
                              colors["aqua"])

    def start_game(self):
        game = game_window.Game(self.display.get_width(), self.display.get_height(), self.field_size,
                                self.computer_play)
        self.running = game.start()

    def show_help(self):
        helping = help_window.Help(self.display.get_width(), self.display.get_height())
        self.running = helping.start()

    def set_small_field(self):
        self.field_size = 4
        self.size_colors = (colors["aqua"], colors["white"], colors["white"])
        self.size_colors_over = (colors["aqua"], colors["aqua"], colors["aqua"])

    def set_medium_field(self):
        self.field_size = field_size
        self.size_colors = (colors["white"], colors["aqua"], colors["white"])
        self.size_colors_over = (colors["aqua"], colors["aqua"], colors["aqua"])

    def set_big_field(self):
        self.field_size = 12
        self.size_colors = (colors["white"], colors["white"], colors["aqua"])
        self.size_colors_over = (colors["aqua"], colors["aqua"], colors["aqua"])

    def set_computer_player(self):
        self.computer_play = True
        self.player_color = (colors["aqua"], colors["white"])
        self.player_color_over = (colors["aqua"], colors["aqua"])

    def set_person_player(self):
        self.computer_play = False
        self.player_color = (colors["white"], colors["aqua"])
        self.player_color_over = (colors["aqua"], colors["aqua"])


if __name__ == "__main__":
    menu = Menu()
    menu.main_cycle()
