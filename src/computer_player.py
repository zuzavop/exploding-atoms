"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import random

import numpy as np

from utils import try_all_neighbours


class Computer:
    def __init__(self, field_size):
        self.optimal = None
        self.maximum = None
        self.number_atoms = None
        self.atoms = None
        self.field_size = field_size
        self.extension = 0
        self.ending = True
        self.copy = []

    def on_turn(self, atoms, numbers):
        self.atoms = atoms
        self.number_atoms = numbers.copy()
        self.maximum = 0
        self.optimal = []

        if self.ending:
            optimal_coord = self.pick_atom()  # approximation of best turn
            if optimal_coord:
                self.optimal = self.atoms[optimal_coord[0]][optimal_coord[1]]
                self.optimal.adding()

    def add(self, atom, number, numbers):
        """ simulation of adding to atom """
        if number > 0:
            if numbers[atom.x][atom.y] < (len(atom.neighbours) - 1):
                self.extension += 1
                numbers[atom.x][atom.y] += 1
            else:
                numbers[atom.x][atom.y] = 0
                for neighbour in atom.neighbours:
                    self.add(neighbour, number - 1, numbers)

    def make_copy(self):
        """ creation of atom copy with current values """
        numbers = np.zeros((self.field_size, self.field_size), dtype=int)
        self.copy = np.empty((self.field_size, self.field_size), dtype=AtomsCopy)

        for x in range(self.field_size):
            for y in range(self.field_size):
                self.copy[x, y] = AtomsCopy([], self.atoms[x, y].text, self.atoms[x, y].color, x, y)
                numbers[x, y] = self.atoms[x, y].text

        try_all_neighbours(self.field_size, self.copy)

        return numbers

    def pick_atom(self):
        """ try simulation adding some atoms and pick the best of them """
        optimal = []
        # find danger atoms of opponent (which can explode in next turn)
        danger_atoms = self.find_danger(1,"blue")
        good_choice = self.find_danger(2, "red")  # find atoms, which can explode in two rounds

        if danger_atoms:
            numbers = self.make_copy()
            self.minimax(good_choice, danger_atoms, self.copy, numbers, 0, [], 3, True, True)
            optimal = self.optimal

        if not optimal:
            """ if none opponents atoms are dangerous or none optimal atom was found
            choose atom that can explode in this turn or in next turn"""
            better_choice = self.find_danger(1, "red")
            if better_choice:
                optimal = random.choice(better_choice)
            else:
                first_choice = self.find_danger(2, "black")
                if first_choice:
                    optimal = random.choice(first_choice)
                elif good_choice:
                    optimal = random.choice(good_choice)
                else:  # if none atom was found - choose randomly
                    last_choice = self.find_danger(4, "red")
                    if last_choice:
                        optimal = random.choice(last_choice)

        return optimal

    def find_danger(self, depth, color, color2="black"):
        """ find atom of given color which can explode in given number of rounds """
        danger = []
        for x in range(self.field_size):
            for y in range(self.field_size):
                atom = self.atoms[x][y]
                if (atom.color == color or atom.color == color2) and (atom.text >= len(atom.neighbours) - depth):
                        danger.append([x, y])
        return danger

    def minimax(self, good_choice, danger_atoms, copy_atoms, atom_numbers, maxi, optim, depth, player, first):
        """ search the best atom for this and next round using minimax"""
        if depth <= 0:
            if maxi > self.maximum:
                self.maximum = maxi
                self.optimal = optim
        else:
            if player:
                hook = [x[:] for x in atom_numbers]
                for atom1 in good_choice:
                    if first:
                        optim = atom1
                    self.extension = 0
                    self.add(copy_atoms[atom1[0]][atom1[1]], self.field_size * self.field_size, atom_numbers)
                    self.minimax(good_choice, danger_atoms, copy_atoms, atom_numbers, maxi + self.extension, optim,
                                 depth - 1, False, False)
                    atom_numbers = hook[:]
            else:
                helper = [x[:] for x in atom_numbers]
                for atom2 in danger_atoms:
                    self.extension = 0
                    self.add(copy_atoms[atom2[0]][atom2[1]], self.field_size * self.field_size, atom_numbers)
                    self.minimax(good_choice, danger_atoms, copy_atoms, atom_numbers, maxi - self.extension, optim,
                                 depth - 1, True, False)
                    atom_numbers = helper[:]


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
