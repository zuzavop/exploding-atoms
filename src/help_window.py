"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame

import button
from setting import hint_text, colors


class Help:
    def __init__(self, width, height):
        pygame.init()

        self.running = True

        # nastaveni velikosti okna
        self.width = width
        self.height = height

        # vytvoreni menitelneho okna s predanymi rozmery
        self.display: pygame.Surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width() // 50)

    def start(self, ending=False):
        """hlavni cyklus Napovedy"""
        hint = []
        shift = self.display.get_height() // 3  # posunuti textu napovedy
        for line in hint_text:  # nacteni textu napovedy a nastaveni jeho polohy v okne
            self.show_help(shift, hint, line)
            shift += self.display.get_height() // 15

        bg = pygame.image.load("..\\res\\universe.jpg")
        picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))

        # vytvoreni zpetneho tlacitka
        back_button = button.Button("Zpět", "white", colors["aqua"], self.back)

        while self.running:
            # nastaveni pozadi
            self.display.blit(picture, (0, 0))

            for a in range(len(hint)):  # zobrazeni textu
                self.display.blit(hint[a][0], hint[a][1])

            back_button.show(self.display, self.display.get_width() - (self.display.get_width() / 20),
                      self.display.get_height() // 100, self.display.get_width() // 7,
                      self.display.get_height() // 10)

            for event in pygame.event.get():  # kontrola novych pygame udalosti
                if event.type == pygame.QUIT:
                    ending = True  # uzavreni okna menu
                    self.back()

                elif event.type == pygame.VIDEORESIZE:  # zmena velikosti okna - prenastaveni rozmeru
                    self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width() // 50)
                    picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
                    shift = self.display.get_height() // 3
                    hint = []
                    for line in hint_text:
                        self.show_help(shift, hint, line)
                        shift += self.display.get_height() // 15

            pygame.display.update()

        if ending:
            return False  # ukonceni menu okna
        else:
            return True

    def show_help(self, shift, hint, line):
        text = self.font.render(line, True, "white")
        text_rect = text.get_rect()
        text_rect.center = (self.display.get_width() // 2, shift)
        hint.append([text, text_rect])

    def back(self):
        """ukonceni aktualniho okna napovedy"""
        self.running = False
