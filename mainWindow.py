"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21

Hlavní čast
Zajištění nastavení hry a přechodů do hry a nápovědy
"""

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
#kvuli skrytí vyzvy od pygame

import pygame

import gameWindow
import helpWindow
import button

#nastaveni barev
aqua = (114, 242, 208)

class Menu:
    def __init__(self):
        #inicializace pygame
        pygame.init()

        #nastaveni preferovanych oteviracich rozmeru
        self.width = 1000
        self.height = 700

        self.running = True
        self.computer_play = False

        #rozmer pole
        self.field_size = 8
        #nastaveni barev tlacitek
        self.color11, self.color22, self.color31 = "white", aqua, "white"
        self.color12, self.color21, self.color32 = aqua, aqua, aqua
        self.color41, self.color51 = "white", aqua
        self.color42, self.color52 = aqua, aqua

        #vytvoreni menitelneho okna o preferovanych rozmerech
        self.display: pygame.Surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        #nastaveni fontu
        self.font = pygame.font.Font('res/font_title.ttf', self.display.get_width()//20)
        
        
    def start(self):
        """hlavni cyklus, ktery vykresluje menu"""

        #nacteni pozadi
        bg = pygame.image.load("res/universe.jpg")
        picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
        

        #nastaveni parametru nadpisu
        title = self.font.render('Exploding  Atoms', True, "white")
        titleRect = title.get_rect()
        
        while self.running:
            #nastaveni pozadi
            self.display.blit(picture, (0, 0))

            #zobrazeni nadpisu
            titleRect.center = (self.display.get_width()//2, 1.5*self.display.get_height()//8)
            self.display.blit(title, titleRect)

            #vytvoreni tlacitek v menu - jelikoz tlacitka se tvori ve vsech oknech tak jsou vytvareny pomoci tridy Button
            button.Button(self.display, "Start", self.display.get_width()//2, 3.2*self.display.get_height()//8, self.display.get_width()//6, self.display.get_height()//9, "black", "white", self.game, "white", aqua)
            
            if not self.running:
                #pokud je hra zavřena v hracím okně, tak aby cyklus dal nepokračoval
                break

            button.Button(self.display, "Proti počítači", 3*self.display.get_width()//8, 5.4*self.display.get_height()//8, self.display.get_width()//5, self.display.get_height()//16, "black", "black", self.computer, self.color41, self.color42, 42)
            button.Button(self.display, "Proti protihráči", 5*self.display.get_width()//8, 5.4*self.display.get_height()//8, self.display.get_width()//5, self.display.get_height()//16, "black", "black", self.person, self.color51, self.color52, 42)
            

            button.Button(self.display, "4x4", 3*self.display.get_width()//8, 4.5*self.display.get_height()//8, self.display.get_width()//12, self.display.get_height()//16, "black", "black", self.small, self.color11, self.color12, 42)
            button.Button(self.display, "8x8", self.display.get_width()//2, 4.5*self.display.get_height()//8, self.display.get_width()//12, self.display.get_height()//16, "black", "black", self.medium, self.color21, self.color22, 42)
            button.Button(self.display, "12x12", 5*self.display.get_width()//8, 4.5*self.display.get_height()//8, self.display.get_width()//12, self.display.get_height()//16, "black", "black", self.big, self.color31, self.color32, 42)

            button.Button(self.display, "Pravidla", self.display.get_width()//2, 6.5*(self.display.get_height()//8), self.display.get_width()//6, self.display.get_height()//9, "black", "white", self.help, "white", aqua)

            for event in pygame.event.get():    #kontrola pygame event a vyvolani reakce na ne
                if event.type == pygame.QUIT: #uzavreni hry
                    self.running = False 

                elif event.type == pygame.VIDEORESIZE: #zmena velikosti okna
                    self.font = pygame.font.Font('res/font_title.ttf', self.display.get_width()//20)
                    picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
                    title = self.font.render('Exploding  Atoms', True, "white")
                    titleRect = title.get_rect()
   

            pygame.display.update() 
        

    def game(self):
        """spusteni hry"""
        game = gameWindow.Game(self.display.get_width(), self.display.get_height(), self.field_size, self.computer_play)
        self.running = game.start()


    def help(self):
        """spusteni napovedy"""
        helping = helpWindow.Help(self.display.get_width(), self.display.get_height())
        self.running = helping.start()


    #inicializace prenastaveni barev tlacitek a velikosti hraciho pole
    def small(self):
        self.field_size = 4
        self.color12, self.color21, self.color31 = aqua, "white", "white"
        self.color11, self.color22, self.color32 = aqua, aqua, aqua
    def medium(self):
        self.field_size = 8
        self.color11, self.color22, self.color31 = "white", aqua, "white"
        self.color12, self.color21, self.color32 = aqua, aqua, aqua
    def big(self):
        self.field_size = 12
        self.color11, self.color21, self.color32 = "white", "white", aqua
        self.color12, self.color22, self.color31 = aqua, aqua, aqua

    #inicializace prenastaveni barev tlacitek a nastaveni hrace
    def computer(self):
        self.computer_play = True
        self.color41, self.color51 = aqua, "white"
        self.color42, self.color52 = aqua, aqua
    def person(self):
        self.computer_play = False
        self.color41, self.color51 = "white", aqua
        self.color42, self.color52 = aqua, aqua


if __name__ == "__main__":
    menu = Menu()
    menu.start()