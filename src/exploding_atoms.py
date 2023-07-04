"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21

"""

import pygame

import main_window

# set name and icon of game
programIcon = pygame.image.load('..\\res\\icon.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption("Exploding Atoms")

# start menu window
menu = main_window.Menu()
menu.main_cycle()
