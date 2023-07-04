"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame


class Button:
    def __init__(self, title, text_color, text_color_over, action=None, font_size=34):
        """vytvoreni tlacitka ktere po kliknuti provede predanou funkci action"""
        self.title = title
        self.text_color = text_color
        self.text_color_over = text_color_over
        self.action = action
        self.font_size = font_size

    def show(self, display, x, y, width, height, bc=None, bc_over=None):
        # nastaveni fontu
        small_text = pygame.font.Font("freesansbold.ttf", display.get_width() // self.font_size)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + (width / 2) > mouse[0] > x - (width / 2) and y + height > mouse[1] > y:
            # pokud je mys na souradnicich tlacitka - zmena barev
            if bc_over is not None:
                pygame.draw.rect(display, bc_over, (x - (width / 2), y, width, height))
            text_surf = small_text.render(self.title, True, self.text_color_over)
            if click[0] == 1 and self.action is not None:  # po kliknuti na tlacitko se provede predana funkce
                self.action()
        else:
            if bc is not None:
                pygame.draw.rect(display, bc, (x - (width / 2), y, width, height))
            text_surf = small_text.render(self.title, True, self.text_color)

        text_rect = text_surf.get_rect()
        text_rect.center = (x, y + (height / 2))
        display.blit(text_surf, text_rect)  # vykresleni tlacitka

    def change_title(self, title):
        self.title = title
