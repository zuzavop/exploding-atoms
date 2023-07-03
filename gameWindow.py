"""
Exploding Atoms

Zuzana Vopálková, 1. ročník

Programování 1 (NPRG030)
zimní semestr 2020/21
"""

import atoms
import button
import computer_player

import pygame

#nastaveni barev
aqua = (114, 242, 208)
red = (255, 36, 36)

class Counter:
    """trida pomoci ktere se urcuje kdo je na tahu"""
    def __init__(self):
        self.counter = 0

    def draw(self):
        self.counter = (self.counter+1)%2


class Game:
    def __init__(self, width, height, field_size, computer_play):
        pygame.init()
        self.running = True

        # nastaveni velikosti okna a velikosti pole - predane z menu
        self.width = width
        self.height = height
        self.field_size = field_size

        #vytvoreni menitelneho okna s predanymi velikostmi
        self.display: pygame.Surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        #nastaveni fontu
        self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width()//(self.field_size*5))

        #nastaveni napisu
        self.title = self.font.render('Na tahu je první hráč', True, aqua)
        self.text = self.font.render('', True, aqua)

        #knihovna urcujici pocet zabarvenych poli
        self.numbers = {"black":self.field_size*self.field_size, "red":0, "blue":0}
        #list s odkazy na tlacitka pole (atomy)
        self.atoms = []
        self.counter = Counter()
        #zajistuje aby bylo zavreno i menu po uravreni hraciho okna
        self.end_game = False

        self.computer_play = computer_play
        self.computer = computer_player.Computer(self.field_size)
        
    def start(self, ending=False):
        """cyklus hry"""
        self.buttons()

        bg = pygame.image.load("res/universe.jpg")
        picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))

        #nastaveni velikosti a zakladni souradnice molekul
        size = self.display.get_height()//int(self.field_size*1.7)
        currentx, currenty = (self.display.get_width()//2-(self.field_size/2)*(size+10))+5, self.display.get_height()//2 - (self.field_size/2)*(size+10) + self.display.get_height()//100

        while self.running:
            self.display.blit(picture, (0, 0)) #nastaveni pozadi

            #kontrola aktualniho hrace a zobrazeni napisu urcujiciho kdo je na tahu
            self.change(self.counter.counter)
            self.display.blit(self.title, (self.display.get_width()//2 - self.title.get_rect().width//2, self.display.get_height()//30))

            #vytvoreni zpetneho tlacitka
            button.Button(self.display, "Zpět", self.display.get_width()-(self.display.get_width()/20), self.display.get_height()//100, self.display.get_width()//7, self.display.get_height()//10, "white", aqua, self.exit)

            #zobrazovani pole s atomy
            x1, y1 = currentx, currenty
            for x in range(len(self.atoms)):
                for a in range(len(self.atoms[x])):
                    self.atoms[x][a].run(size, x1, y1)
                    x1 += size + 10
                x1 = currentx
                y1 += size + 10
    
            self.win_check() #kontrola vyhry
            if self.counter.counter == 1 and self.computer_play:
                pygame.display.update() #kvuli zobrazeni napisu ze je na tahu pocitac
                pygame.time.wait(100)
                self.computer.on_turn(self.atoms, self.numbers)

            for event in pygame.event.get(): #prochazi nove pygame udalosti
                if event.type == pygame.QUIT:
                    ending = True #kvuli uzavreni menu okna
                    self.exit()

                elif event.type == pygame.VIDEORESIZE: #zmena velikosti okna
                    self.font = pygame.font.Font('freesansbold.ttf', self.display.get_width()//43)
                    picture = pygame.transform.scale(bg, (self.display.get_width(), self.display.get_height()))
                    size = self.display.get_height()//int(self.field_size*1.7)
                    currentx, currenty = (self.display.get_width()//2-(self.field_size/2)*(size+10))+5, self.display.get_height()//2 - (self.field_size/2)*(size+10) + self.display.get_height()//100
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #konrola kliknuti leveho tlacitka mysi
                    if self.end_game: #po ukonceni hry inicializuje po kliknuti navrat do menu
                        self.running = False
                    else:
                        for x in range(len(self.atoms)):
                            for a in range(len(self.atoms[x])):
                                self.atoms[x][a].clicked() #hledani zmacknuteho atomu a pripadna inicializace zvetseni poctu castic v atomu
                        

            pygame.display.update() 

        if ending: #inicializuje uzavreni menu
            return False
        else: #navrat do menu
            return True

     
    def change(self, counter):
        """po odehrani hrace zmeni napis s aktualnim hracem"""
        if counter == 1:
            self.title = self.font.render('Na tahu je druhý hráč', True, red)
            if self.computer_play:
                self.title = self.font.render('Na tahu je počítač', True, red)
        else:
            self.title = self.font.render('Na tahu je první hráč', True, aqua)

    def win_check(self):
        """kontrola jestli nekdo jiz nevyhral a pripadne ukonceni aktualni hry"""
        if self.numbers["red"] >= self.field_size*self.field_size:
            if self.computer_play:
                self.win("počítač", red)
            else:
                self.win("druhý hráč", red)
        elif self.numbers["blue"] >= self.field_size*self.field_size:
            self.win("první hráč", aqua)

    def exit(self):
        """ukonceni aktualniho okna"""
        self.running = False

    def win(self, winner, color):
        """ukaze vyherce a po kliknuti ukonci hru"""
        self.title = self.font.render('', True, color) #aby se nezobrazoval napis aktualniho hrace

        #nastaveni castecne pruhledne plochy pres cele okno
        s = pygame.Surface((self.display.get_width(), self.display.get_height()), pygame.SRCALPHA)
        s.fill((255, 255, 255, 220))
        self.display.blit(s, (0, 0))

        #nastaveni napisu vyherce
        self.text = self.font.render(f'Výhercem se stal {winner}', True, color)
        self.display.blit(self.text, (self.display.get_width()//2 - self.text.get_rect().width//2, self.display.get_height()//2 - self.text.get_rect().height//2))
        
        #znemozni klikani na tlacitka molekul a naopak po kliknuti inicializuje navrat do menu
        self.end_game = True 

    def buttons(self):
        """vytvoreni pole s tlacitky neboli atomy a prirazeni jejich sousedu"""

        for x in range(self.field_size):
            helper = [] #pomocna promenna - umoznuje ukladani tlacitek do listu (self.atoms) po radcich
            for a in range(self.field_size):
                b = atoms.Atom(self.display, self.counter, 0, [], self.numbers, self.field_size)
                helper += [b]
                
            self.atoms.append(helper) #pridani radku do listu
        
        move = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        
        for x in range(self.field_size): #vyzkouseni vsech moznych sousedu
            for a in range(self.field_size):
                for heave in range(len(move)):
                    current_x = x + move[heave][0]
                    current_a = a + move[heave][1]
                    if (current_x < self.field_size) and (current_x >= 0) and (current_a < self.field_size) and (current_a >= 0):
                        self.atoms[x][a].addNeighbour(self.atoms[current_x][current_a]) #pridani souseda k atomu

if __name__ == "__main__": #pokud by bylo rovnou spusteno hraci pole
    game = Game(1000, 700, 8)
    game.start()