"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame

from setting import colors


class Atom:
    def __init__(self, display, counter, text, neighbours, atoms: dict, field_size):
        self.display = display
        self.neighbours = neighbours
        self.text = text
        self.counter = counter
        self.color = "black"
        self.atoms = atoms
        self.field_size = field_size
        self.x, self.y, self.size = 0, 0, 0  # hned se do nich dosadi v self.run

    def run(self, size, x, y):
        """vykresleni tlacitka (molekuly) na display"""
        self.x = x
        self.y = y
        self.size = size

        pygame.draw.rect(self.display, colors["white"], (x, y, size, size))

        small_text = pygame.font.Font("freesansbold.ttf", size // 2)
        text_surf = small_text.render(f" {self.text} ", True, colors[self.color])
        text_rect = text_surf.get_rect()
        text_rect.center = ((x + (size // 2)), (y + (size // 2)))

        self.display.blit(text_surf, text_rect)

    def clicked(self):
        """kontrola polohy mysi po zmacknuti"""
        mouse = pygame.mouse.get_pos()
        if self.x + self.size > mouse[0] > self.x and self.y + self.size > mouse[1] > self.y:
            if not ((self.counter.counter == 1 and self.color == 'blue') or (
                    self.counter.counter == 0 and self.color == 'red')):
                # kontrola jestli se souper nesnazi zmacknout tlacitko, ktere je obarveno souperovou barvou
                self.adding()  # pokud bylo zmacknuto toto tlacitko tak se zvetsi cislo

    def adding(self, coloring=""):
        """zvetseni cisla na tlacitku
        pokud je stejne jako pocet sousedu tak exploduje
        urcuje barvu tlacitka pokud se jedna o prvni obarveni 
        pokud jde o explozi tak je predana barva puvodni explodovaneho atomu pomoci coloring"""
        tah = False
        if coloring == "":
            if self.color == "black":
                if self.counter.counter == 0:
                    self.color = 'blue'
                else:
                    self.color = 'red'
                self.atoms[self.color] += 1  # zaznamenani, ze pribylo jedno tlacitko teto barvy

            tah = True  # vytvoreni "dluhu" tahu - kvuli tomu aby se provedl az po dokonceni explozi

        else:
            self.atoms[self.color] -= 1  # zmena zaznamu o barve tlacitka
            self.color = coloring  # nastaveni barvy tlacitka pri expozi
            self.atoms[self.color] += 1

        if self.text < len(self.neighbours) - 1:  # zvetseni poctu castic pokud jich tam neni jako pocet sousedu
            self.text += 1
        else:
            self.explode()  # exploze atomu

        if tah:
            self.counter.draw()  # provedeni tahu

    def add_neighbour(self, neighbour):
        """pridani souseda atomu"""
        self.neighbours.append(neighbour)

    def explode(self):
        """pokud se nejedna o vitezny tah tak prerozdeli castice z aktualniho atomu do sousedu"""
        if self.atoms["red"] < self.field_size * self.field_size and self.atoms[
            "blue"] < self.field_size * self.field_size:
            self.text = 0
            for a in range(len(self.neighbours)):
                self.neighbours[a].adding(self.color)
