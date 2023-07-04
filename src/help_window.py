"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame

import button

aqua = (114, 242, 208)
# nastaveni textu napovedy - slo by urcite udelat lepe, ale diky tomuto zpusobu bylo jednoduche menit radkovani a tedy zaplnit celou obrazovku
hint_text = ["Hráči střídavě vybírají políčka neboli atomy z hracího plánu. Nelze zvolit atom,",
             "který je již zabran soupeřem. Když je atom NAPLNĚN, tj. obsahuje dostatečný počet",
             "částic (tak velké číslo, jako má políčko sousedních políček - tedy podle umístění políčka",
             "čísla 2, 3 nebo 4), exploduje a rozdělí se mezi sousední atomy. Případné soupeřovy částice,",
             "které tam již byly, přebarví na svou barvu. Soupeřovi vlastní atomy zůstávají a pokud je atom",
             "znovu naplněn následuje další exploze. Vyhrává hráč, který eliminuje soupeře,",
             "tedy jinak řečeno dokáže obarvit celé hrací pole svou barvou."]


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
        for a in hint_text:  # nacteni textu napovedy a nastaveni jeho polohy v okne
            text = self.font.render(a, True, "white")
            text_rect = text.get_rect()
            text_rect.center = (self.display.get_width() // 2, shift)
            hint.append([text, text_rect])
            shift += self.display.get_height() // 15

        bg = pygame.image.load("res/universe.jpg")
        picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))

        while self.running:
            # nastaveni pozadi
            self.display.blit(picture, (0, 0))

            for a in range(len(hint)):  # zobrazeni textu
                self.display.blit(hint[a][0], hint[a][1])

            # vytvoreni zpetneho tlacitka
            button.Button(self.display, "Zpět", self.display.get_width() - (self.display.get_width() / 20),
                          self.display.get_height() // 100, self.display.get_width() // 7,
                          self.display.get_height() // 10, "white", aqua, self.back)

            for event in pygame.event.get():  # kontrola novych pygame udalosti
                if event.type == pygame.QUIT:
                    ending = True  # uzavreni okna menu
                    self.back()

                elif event.type == pygame.VIDEORESIZE:  # zmena velikosti okna - prenastaveni rozmeru
                    self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width() // 50)
                    picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
                    shift = self.display.get_height() // 3
                    hint = []
                    for a in hint_text:
                        text = self.font.render(a, True, "white")
                        text_rect = text.get_rect()
                        text_rect.center = (self.display.get_width() // 2, shift)
                        hint.append([text, text_rect])
                        shift += self.display.get_height() // 15

            pygame.display.update()

        if ending:
            return False  # ukonceni menu okna
        else:
            return True

    def back(self):
        """ukonceni aktualniho okna napovedy"""
        self.running = False
