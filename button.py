"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame

class Button:
    def __init__(self, display, msg, x, y, w, h, color1, color2, action=None, bc=None, ac=None, size=34):
        """vytvoreni tlacitka ktere po kliknuti provede predanou funkci action"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #nastaveni fontu
        smallText = pygame.font.Font("freesansbold.ttf", display.get_width()//size)
        
        if x+(w/2) > mouse[0] > x-(w/2) and y+h > mouse[1] > y: #pokud je mys na souradnicich tlacitka - zmena barev
            if bc != None:
                pygame.draw.rect(display, ac, (x-(w/2), y, w, h))
            textSurf = smallText.render(msg, True, color2)
            if click[0] == 1 and action != None: #po kliknuti na tlacitko se provede predana funkce
                action()         
        else:
            if bc != None:
                pygame.draw.rect(display, bc, (x-(w/2), y, w, h))
            textSurf = smallText.render(msg, True, color1)
        
        textRect = textSurf.get_rect()
        textRect.center = (x, y+(h/2))
        display.blit(textSurf, textRect) #vykresleni tlacitka
        
        

