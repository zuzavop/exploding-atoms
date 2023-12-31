"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame

from src.utils import is_clicked_button


class Button:
    def __init__(self, title, text_color, text_color_over, action=None, font_size=34):
        """ creates a button that performs the passed action when clicked """
        self.title = title
        self.text_color = text_color
        self.text_color_over = text_color_over
        self.action = action
        self.font_size = font_size

    def show(self, display, x, y, width, height, bc=None, bc_over=None):
        """ displays the button on the given display at the specified position and size """
        # set font
        small_text = pygame.font.Font("freesansbold.ttf", display.get_width() // self.font_size)

        click = pygame.mouse.get_pressed()

        if is_clicked_button(x - (width / 2), y, width, height):
            # if mouse is on the button coordinates - change colors
            if bc_over is not None:
                pygame.draw.rect(display, bc_over, (x - (width / 2), y, width, height))
            text_surf = small_text.render(self.title, True, self.text_color_over)
            if click[0] == 1 and self.action is not None:  # execute the action when button is clicked
                self.action()
        else:
            if bc is not None:
                pygame.draw.rect(display, bc, (x - (width / 2), y, width, height))
            text_surf = small_text.render(self.title, True, self.text_color)

        text_rect = text_surf.get_rect(center=(x, y + (height / 2)))
        display.blit(text_surf, text_rect)  # draw the button

    def change_title(self, title):
        """ changes the title of the button """
        self.title = title
