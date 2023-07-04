"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21

"""

import pygame

import main_window

# nastaveni ikony a nazvu hry
programIcon = pygame.image.load('..\res\icon.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Exploding Atoms")

# spusteni hlavniho okna s menu
menu = main_window.Menu()
menu.start()
