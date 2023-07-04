"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import pygame

import atoms
import button
import computer_player
from setting import colors


class Counter:
    """ use for deciding who's turn is now """
    def __init__(self):
        self.counter = 0

    def draw(self):
        self.counter = (self.counter + 1) % 2


class Game:
    def __init__(self, width, height, field_size, computer_play):
        pygame.init()
        self.running = True

        # set size from menu
        self.width = width
        self.height = height
        self.field_size = field_size

        # create window
        self.display: pygame.Surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        # set font
        self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width() // (self.field_size * 5))

        # set title
        self.title = self.font.render('Na tahu je první hráč', True, colors["aqua"])
        self.text = self.font.render('', True, colors["aqua"])

        self.numbers = {"black": self.field_size * self.field_size, "red": 0, "blue": 0}
        self.atoms = []
        self.counter = Counter()
        self.end_game = False

        self.computer_play = computer_play
        self.computer = computer_player.Computer(self.field_size)

    def start(self, ending=False):
        """ game cycle """
        self.buttons()

        bg = pygame.image.load("..\\res\\universe.jpg")
        picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))

        # set size and coordination of atoms
        size = self.display.get_height() // int(self.field_size * 1.7)
        current_x, current_y = (self.display.get_width() // 2 - (self.field_size / 2) * (
                    size + 10)) + 5, self.display.get_height() // 2 - (self.field_size / 2) * (
                                         size + 10) + self.display.get_height() // 100

        # create back button
        back_button = button.Button("Zpět", colors["white"], colors["aqua"], self.exit)

        while self.running:
            self.display.blit(picture, (0, 0))  # set background

            # control current player and set help
            self.change(self.counter.counter)
            self.display.blit(self.title, (
            self.display.get_width() // 2 - self.title.get_rect().width // 2, self.display.get_height() // 30))

            back_button.show(self.display, self.display.get_width() - (self.display.get_width() / 20),
                      self.display.get_height() // 100, self.display.get_width() // 7,
                      self.display.get_height() // 10)

            # field with atoms
            x1, y1 = current_x, current_y
            for x in range(len(self.atoms)):
                for a in range(len(self.atoms[x])):
                    self.atoms[x][a].run(size, x1, y1)
                    x1 += size + 10
                x1 = current_x
                y1 += size + 10

            self.win_check()  # control of end
            if self.counter.counter == 1 and self.computer_play:
                pygame.display.update()  # because of title that computer is on turn
                pygame.time.wait(100)
                self.computer.on_turn(self.atoms, self.numbers)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ending = True
                    self.exit()

                elif event.type == pygame.VIDEORESIZE:  # change of window size
                    self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width() // 43)
                    picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
                    size = self.display.get_height() // int(self.field_size * 1.7)
                    current_x, current_y = (self.display.get_width() // 2 - (self.field_size / 2) * (
                                size + 10)) + 5, self.display.get_height() // 2 - (self.field_size / 2) * (
                                                     size + 10) + self.display.get_height() // 100

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left button click
                    if self.end_game:  # after game end initialize return to menu
                        self.running = False
                    else:
                        for x in range(len(self.atoms)):
                            for a in range(len(self.atoms[x])):
                                self.atoms[x][a].clicked()  # find clicked atom

            pygame.display.update()

        if ending:
            return False
        else:  # return to menu
            return True

    def change(self, counter):
        """ change helper text after player turn """
        if counter == 1:
            self.title = self.font.render('Na tahu je druhý hráč', True, colors["red"])
            if self.computer_play:
                self.title = self.font.render('Na tahu je počítač', True, colors["red"])
        else:
            self.title = self.font.render('Na tahu je první hráč', True, colors["aqua"])

    def win_check(self):
        """ control of end of game """
        if self.numbers["red"] >= self.field_size * self.field_size:
            if self.computer_play:
                self.win("počítač", colors["red"])
            else:
                self.win("druhý hráč", colors["red"])
        elif self.numbers["blue"] >= self.field_size * self.field_size:
            self.win("první hráč", colors["aqua"])

    def exit(self):
        """ close of current window """
        self.running = False

    def win(self, winner, color):
        """ show winner and after click end game """
        self.title = self.font.render('', True, color)

        # set window color
        s = pygame.Surface((self.display.get_width(), self.display.get_height()), pygame.SRCALPHA)
        s.fill((255, 255, 255, 220))
        self.display.blit(s, (0, 0))

        # set name winner
        self.text = self.font.render(f'Výhercem se stal {winner}', True, color)
        self.display.blit(self.text, (self.display.get_width() // 2 - self.text.get_rect().width // 2,
                                      self.display.get_height() // 2 - self.text.get_rect().height // 2))

        self.end_game = True

    def buttons(self):
        """ create field with atoms """

        for x in range(self.field_size):
            helper = []
            for a in range(self.field_size):
                b = atoms.Atom(self.display, self.counter, 0, [], self.numbers, self.field_size)
                helper += [b]

            self.atoms.append(helper)  # add line to list

        move = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        for x in range(self.field_size):  # try all neighbours
            for a in range(self.field_size):
                for heave in range(len(move)):
                    current_x = x + move[heave][0]
                    current_a = a + move[heave][1]
                    if (current_x < self.field_size) and (current_x >= 0) and (current_a < self.field_size) and (
                            current_a >= 0):
                        self.atoms[x][a].add_neighbour(self.atoms[current_x][current_a])  # add neighbour to atom


if __name__ == "__main__":
    game = Game(1000, 700, 8, 1)
    game.start()
