"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame

import button
from setting import hint_text, colors, background_path


class Help:
    def __init__(self, width, height):
        pygame.init()

        self.running = True

        # set window size
        self.width = width
        self.height = height

        # create window
        self.display: pygame.Surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width() // 50)

    def start(self, ending=False):
        """ main cycle of Help """
        hint = []
        shift = self.display.get_height() // 3  # shift text of help
        for line in hint_text:
            self.show_help(shift, hint, line)
            shift += self.display.get_height() // 15

        bg = pygame.image.load(background_path)
        picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))

        back_button = button.Button("Zpět", "white", colors["aqua"], self.back)

        while self.running:
            # set background
            self.display.blit(picture, (0, 0))

            for a in range(len(hint)):  # show text
                self.display.blit(hint[a][0], hint[a][1])

            back_button.show(self.display, self.display.get_width() - (self.display.get_width() / 20),
                      self.display.get_height() // 100, self.display.get_width() // 7,
                      self.display.get_height() // 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ending = True
                    self.back()

                elif event.type == pygame.VIDEORESIZE:  # change window size
                    self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width() // 50)
                    picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
                    shift = self.display.get_height() // 3
                    hint = []
                    for line in hint_text:
                        self.show_help(shift, hint, line)
                        shift += self.display.get_height() // 15

            pygame.display.update()

        if ending:
            return False
        else:
            return True

    def show_help(self, shift, hint, line):
        text = self.font.render(line, True, "white")
        text_rect = text.get_rect()
        text_rect.center = (self.display.get_width() // 2, shift)
        hint.append([text, text_rect])

    def back(self):
        """ end current window """
        self.running = False
