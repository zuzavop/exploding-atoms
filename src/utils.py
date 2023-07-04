import pygame


def try_all_neighbours(field_size, atoms):
    move = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    for x in range(field_size):  # try all neighbours
        for y in range(field_size):
            for dx, dy in move:
                current_x = x + dx
                current_y = y + dy
                if 0 <= current_x < field_size and 0 <= current_y < field_size:
                    atoms[x][y].add_neighbour(atoms[current_x][current_y])  # add neighbour to atom


def is_clicked_button(x, y, w, h):
    mouse_pos = pygame.mouse.get_pos()
    return x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h


class Counter:
    """ use for deciding who's turn is now """

    def __init__(self):
        self.counter = 0

    def draw(self):
        self.counter = (self.counter + 1) % 2

    def is_blue_turn(self):
        return self.counter == 0

    def is_red_turn(self):
        return self.counter == 1


class AtomsCopy:
    """ atom copy with needed values - for computing """

    def __init__(self, neighbours, text, color, x, y):
        self.neighbours = neighbours
        self.text = text
        self.color = color
        self.x = x
        self.y = y

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
