"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21

"""

import mainWindow
import pygame

#nastaveni ikony a nazvu hry
programIcon = pygame.image.load('res\icon.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Exploding Atoms")

#spusteni hlavniho okna s menu
menu = mainWindow.Menu()
menu.start()