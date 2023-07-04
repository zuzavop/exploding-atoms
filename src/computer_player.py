"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import random


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

        if self.ending:  # pokud jeste neskoncila hra

            optimal_coor = self.pick_atom()  # odhad nejlepsiho tahu
            if optimal_coor:
                self.optimal = self.atoms[optimal_coor[0]][optimal_coor[1]]
                self.optimal.adding()  # zvetseni hodnoty vybraneho atomu

    def add(self, atom, number, numbers):
        """"simuluje" zvetseni vybraneho atomu"""
        if number > 0:
            if numbers[atom.x][atom.a] < (len(atom.neighbours) - 1):
                self.extension += 1
                numbers[atom.x][atom.a] += 1
            else:
                numbers[atom.x][atom.a] = 0
                for b in range(len(atom.neighbours)):
                    self.add(atom.neighbours[b], number - 1, numbers)

    def make_copy(self):
        """vytvori kopie Atomu s aktualnimi hodnotami, barvami a jejich sousedy"""
        numbers = []
        self.copy = []
        for x in range(self.field_size):
            helper = []
            help_num = []
            for a in range(self.field_size):
                helper.append(AtomsCopy([], self.atoms[x][a].text, self.atoms[x][a].color, x, a))
                help_num.append(self.atoms[x][a].text)
            self.copy.append(helper)
            numbers.append(help_num)

        move = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        for x in range(self.field_size):  # vyzkouseni vsech moznych sousedu
            for a in range(self.field_size):
                for heave in range(len(move)):
                    current_x = x + move[heave][0]
                    current_a = a + move[heave][1]
                    if (current_x < self.field_size) and (current_x >= 0) and (current_a < self.field_size) and (
                            current_a >= 0):
                        self.copy[x][a].add_neighbour(self.copy[current_x][current_a])  # pridani souseda k atomu

        return numbers

    def pick_atom(self):
        """zkousi simulovat zvetsovani nekterych atomu a vybere nejlepsi mozny"""
        optimal = []
        danger_atoms = self.find_danger(1,
                                        "blue")  # najde nebezpecne atomy soupere, tedy ty ktere mohou explodovat v nasledujicim kole
        good_choice = self.find_danger(2, "red")  # najde atomy, ktere mohou explodovat do dvou kol
        if danger_atoms:
            numbers = self.make_copy()
            self.minimax(good_choice, danger_atoms, self.copy, numbers, 0, [], 3, True, True)
            optimal = self.optimal
        if not optimal:
            """pokud nejsou zadne nebezpecne atomy soupere nebo se nepovedlo vybrat optialni atom
            vybere atomy ktere exploduji toto kolo a pokud takove nejsou tak nahodne vybere nejaky 
            ktery jeste neni obarveny a mohl by explodovat do dvou kol
            pokud neni ani takovy vybere nejaky ktery je jiz obarveny a mohl by explodovat do dvou kol"""
            better_choice = self.find_danger(1, "red")
            if better_choice:
                optimal = random.choice(better_choice)
            else:
                first_choice = self.find_danger(2, "black")
                if first_choice:
                    optimal = random.choice(first_choice)
                elif good_choice:
                    optimal = random.choice(good_choice)
                else:  # pokud by ani tak nenasel zadny atom tak se vybere jakykoli volny nebo jiz obarveny, ktery vsak vybuchne az za vice jak 3 kola
                    last_choice = self.find_danger(4, "red")
                    if last_choice:
                        optimal = random.choice(last_choice)
        return optimal

    def find_danger(self, depth, color, color2="black"):
        """najde atomy dane barvy, ktere moho do daneho poctu kol(depth) explodovat"""
        danger = []
        for x in range(self.field_size):
            for a in range(self.field_size):
                if self.atoms[x][a].color == color or self.atoms[x][a].color == color2:
                    if self.atoms[x][a].text >= len(self.atoms[x][a].neighbours) - depth:
                        danger.append([x, a])
        return danger

    def minimax(self, good_choice, danger_atoms, copy_atoms, atom_numbers, maxi, optim, depth, player, first):
        """pomoci algoritmu minimaxu se hleda nejlepsi mozny tah na nasledujici dve kola"""
        if depth <= 0:
            if maxi > self.maximum:
                self.maximum = maxi
                self.optimal = optim
        else:
            if player:
                hook = [x[:] for x in atom_numbers]  # kvuli uplne kopii listu v listu
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
    """kopie atomu pouze z potrebnymi argumenty - aby se nemenili zobrazovane atomy"""

    def __init__(self, neighbours, text, color, x, a):
        self.neighbours = neighbours
        self.text = text
        self.color = color
        self.x = x
        self.a = a

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
