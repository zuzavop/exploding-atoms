"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame

from setting import colors


class Atom:
    def __init__(self, game, text, neighbours):
        self.game = game
        self.neighbours = neighbours
        self.text = text
        self.color = "black"
        self.x, self.y, self.size = 0, 0, 0  # will be assigned in self.run()

    def run(self, size, x, y):
        """ draws the button (molecule) on the display """
        self.x, self.y, self.size = x, y, size

        pygame.draw.rect(self.game.display, colors["white"], (x, y, size, size))

        small_text = pygame.font.Font("freesansbold.ttf", size // 2)
        text_surf = small_text.render(f" {self.text} ", True, colors[self.color])
        text_rect = text_surf.get_rect(center=((x + (size // 2)), (y + (size // 2))))

        self.game.display.blit(text_surf, text_rect)

    def clicked(self):
        """ checks mouse position after clicking """
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.size and self.y < mouse_pos[1] < self.y + self.size:
            # check if opponent tries to click a button of their color
            if not ((self.game.counter.is_red_turn() and self.color == 'blue') or (
                    self.game.counter.is_blue_turn() and self.color == 'red')):
                self.adding()  # increase the number if the button is clicked

    def adding(self, coloring=""):
        """ increases the number on the button
        if it's the same as the number of neighbors, it explodes
        determines the color of the button if it's the first coloring
        if it's an explosion, the original exploded atom's color is passed through coloring parameter"""
        turn_debt = False
        if coloring == "":
            if self.color == "black":
                self.color = 'blue' if self.game.counter.is_blue_turn() else 'red'
                self.game.numbers[self.color] += 1  # update the count of buttons of this color
            turn_debt = True  # create a "turn debt" - to be executed after the explosion is completed
        else:
            self.game.numbers[self.color] -= 1  # update the count of buttons
            self.color = coloring  # set the color of the button during explosion
            self.game.numbers[self.color] += 1

        if self.text < len(self.neighbours) - 1:
            # increase the particle count if it's less than the number of neighbors
            self.text += 1
        else:
            self.explode()  # explode the atom

        if turn_debt:
            self.game.counter.draw()  # perform turn

    def add_neighbour(self, neighbour):
        """ adds a neighbor atom """
        self.neighbours.append(neighbour)

    def explode(self):
        """ redistributes particles from the current atom to its neighbors if it's not a winning move """
        if self.game.numbers["red"] < self.game.field_size * self.game.field_size and \
                self.game.numbers["blue"] < self.game.field_size * self.game.field_size:
            self.text = 0
            for neighbour in self.neighbours:
                neighbour.adding(self.color)
