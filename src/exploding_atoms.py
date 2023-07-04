"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21

"""

import pygame

import main_window
from setting import game_title, icon_path

# set name and icon of game
programIcon = pygame.image.load(icon_path)
pygame.display.set_icon(programIcon)
pygame.display.set_caption(game_title)

# start menu window
menu = main_window.Menu()
menu.main_cycle()
