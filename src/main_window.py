"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21

Hlavní čast
Zajištění nastavení hry a přechodů do hry a nápovědy
"""

from os import environ

from setting import colors, window_width, window_height, field_size

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# kvuli skrytí vyzvy od pygame

import pygame

import game_window
import help_window
import button


class Menu:
    def __init__(self):
        # inicializace pygame
        pygame.init()

        # nastaveni preferovanych oteviracich rozmeru
        self.width = window_width
        self.height = window_height

        self.running = True
        self.computer_play = False

        # rozmer pole
        self.field_size = field_size

        # nastaveni barev tlacitek
        self.color11, self.color22, self.color31 = "white", colors["aqua"], "white"
        self.color12, self.color21, self.color32 = colors["aqua"], colors["aqua"], colors["aqua"]
        self.color41, self.color51 = "white", colors["aqua"]
        self.color42, self.color52 = colors["aqua"], colors["aqua"]

        # vytvoreni menitelneho okna o preferovanych rozmerech
        self.display: pygame.Surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # nastaveni fontu
        self.font = pygame.font.Font('..\\res\\font_title.ttf', self.display.get_width() // 20)

    def main_cycle(self):
        """hlavni cyklus, ktery vykresluje menu"""

        # nacteni pozadi
        bg = pygame.image.load("..\\res\\universe.jpg")
        picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))

        # nastaveni parametru nadpisu
        title = self.font.render('Exploding  Atoms', True, colors["white"])
        title_rect = title.get_rect()

        # vytvoreni tlacitek
        start_button = button.Button("Start", colors["black"], colors["white"], self.start_game)

        against_computer_button = button.Button("Proti počítači", colors["black"], colors["black"],
                                                self.set_computer_player, 42)
        against_person_button = button.Button("Proti protihráči", colors["black"], colors["black"],
                                              self.set_person_player, 42)

        small_display_button = button.Button("4x4", colors["black"], colors["black"], self.set_small_field, 42)
        medium_display_button = button.Button("8x8", colors["black"], colors["black"], self.set_medium_field, 42)
        big_display_button = button.Button("12x12", colors["black"], colors["black"], self.set_big_field, 42)

        help_button = button.Button("Pravidla", colors["black"], colors["black"], self.show_help)

        while self.running:
            # nastaveni pozadi
            self.display.blit(picture, (0, 0))

            # zobrazeni nadpisu
            title_rect.center = (self.display.get_width() // 2, 1.5 * self.display.get_height() // 8)
            self.display.blit(title, title_rect)

            start_button.show(self.display, self.display.get_width() // 2, 3.2 * self.display.get_height() // 8,
                              self.display.get_width() // 6, self.display.get_height() // 9, colors["white"],
                              colors["aqua"])

            if not self.running:  # pokud je hra zavřena v hracím okně
                break

            # zobrazeni tlacitek
            against_computer_button.show(self.display, 3 * self.display.get_width() // 8,
                                         5.4 * self.display.get_height() // 8, self.display.get_width() // 5,
                                         self.display.get_height() // 16, self.color41, self.color42)
            against_person_button.show(self.display, 5 * self.display.get_width() // 8,
                                       5.4 * self.display.get_height() // 8, self.display.get_width() // 5,
                                       self.display.get_height() // 16, self.color51, self.color52)
            small_display_button.show(self.display, 3 * self.display.get_width() // 8,
                                      4.5 * self.display.get_height() // 8,
                                      self.display.get_width() // 12, self.display.get_height() // 16, self.color11,
                                      self.color12)
            medium_display_button.show(self.display, self.display.get_width() // 2,
                                       4.5 * self.display.get_height() // 8,
                                       self.display.get_width() // 12, self.display.get_height() // 16, self.color21,
                                       self.color22)
            big_display_button.show(self.display, 5 * self.display.get_width() // 8,
                                    4.5 * self.display.get_height() // 8, self.display.get_width() // 12,
                                    self.display.get_height() // 16, self.color31, self.color32)
            help_button.show(self.display, self.display.get_width() // 2, 6.5 * (self.display.get_height() // 8),
                             self.display.get_width() // 6, self.display.get_height() // 9, colors["white"],
                             colors["aqua"])

            for event in pygame.event.get():  # kontrola pygame event a vyvolani reakce
                if event.type == pygame.QUIT:  # uzavreni hry
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:  # zmena velikosti okna
                    self.font = pygame.font.Font('..\\res\\font_title.ttf', self.display.get_width() // 20)
                    picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
                    title = self.font.render('Exploding  Atoms', True, colors["white"])
                    title_rect = title.get_rect()

            pygame.display.update()

    def start_game(self):
        game = game_window.Game(self.display.get_width(), self.display.get_height(), self.field_size,
                                self.computer_play)
        self.running = game.start()

    def show_help(self):
        helping = help_window.Help(self.display.get_width(), self.display.get_height())
        self.running = helping.start()

    # inicializace prenastaveni barev tlacitek a velikosti hraciho pole
    def set_small_field(self):
        self.field_size = 4
        self.color12, self.color21, self.color31 = colors["aqua"], colors["white"], colors["white"]
        self.color11, self.color22, self.color32 = colors["aqua"], colors["aqua"], colors["aqua"]

    def set_medium_field(self):
        self.field_size = field_size
        self.color11, self.color22, self.color31 = colors["white"], colors["aqua"], colors["white"]
        self.color12, self.color21, self.color32 = colors["aqua"], colors["aqua"], colors["aqua"]

    def set_big_field(self):
        self.field_size = 12
        self.color11, self.color21, self.color32 = colors["white"], colors["white"], colors["aqua"]
        self.color12, self.color22, self.color31 = colors["aqua"], colors["aqua"], colors["aqua"]

    # inicializace prenastaveni barev tlacitek a nastaveni hrace
    def set_computer_player(self):
        self.computer_play = True
        self.color41, self.color51 = colors["aqua"], colors["white"]
        self.color42, self.color52 = colors["aqua"], colors["aqua"]

    def set_person_player(self):
        self.computer_play = False
        self.color41, self.color51 = colors["white"], colors["aqua"]
        self.color42, self.color52 = colors["aqua"], colors["aqua"]


if __name__ == "__main__":
    menu = Menu()
    menu.main_cycle()