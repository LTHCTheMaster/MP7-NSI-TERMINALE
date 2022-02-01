from os import name, system, listdir, path
from time import sleep
from keyboard import is_pressed

# Class Lemming
class Lemming:
    def __init__(self, origin_l: int, origin_c: int) -> None:
        self.l = origin_l
        self.c = origin_c
        self.d = 1 # 1 = droite, -1 = gauche
    
    def avancer(self):
        try:
            if game.grille[self.l][self.c+self.d].estLibre() and not game.grille[self.l][self.c+self.d].estObstruee():
                game.grille[self.l][self.c].liberer()
                game.grille[self.l][self.c+self.d].occuper(self)
                self.c += self.d
            else:
                self.retourner()
        except:
            self.retourner()
    
    def retourner(self):
        self.d *= -1

    def tomber(self):
        try:
            if game.grille[self.l+1][self.c].estLibre() and not game.grille[self.l+1][self.c].estObstruee():
                game.grille[self.l][self.c].liberer()
                game.grille[self.l+1][self.c].occuper(self)
                self.l += 1
            else:
                self.avancer()
        except:
            self.avancer()
    
    def __str__(self) -> str:
        if self.d == 1:
            return '> '
        else:
            return '< '

# Class Case
class Case:
    """The Case class"""
    def __init__(self, terrain: str = ' '):
        self.terrain: str = terrain
        self.lemming: Lemming = None
    
    def estLibre(self) -> bool:
        return self.lemming is None
    
    def estObstruee(self) -> bool:
        return self.terrain == '#'
    
    def liberer(self):
        if not self.estObstruee() and not self.estLibre():
            self.lemming = None
    
    def isOrigin(self) -> bool:
        return self.terrain == 'I'
    
    def isExit(self) -> bool:
        return self.terrain == 'O'
    
    def occuper(self, lemming: Lemming):
        if not self.estObstruee() and self.estLibre():
            self.lemming = lemming

    def __str__(self) -> str:
        if self.lemming is None:
            return self.terrain + " "
        else:
            return str(self.lemming)

# Map Loader
def map_loader(path: str) -> tuple[list[list[Case]],str,tuple[int, int], tuple[int, int]]:
    out_map: list[list[Case]] = []
    file = open(path, 'r+')
    file.write('')
    name = file.readline()[9:].replace('\n','')
    map_raw = file.readlines()
    for i in map_raw:
        add = []
        for j in i.replace('\n',''):
            add.append(Case(j))
        out_map.append(add.copy())
    origin_point = None
    exit_point = None
    for i in range(len(out_map)):
        for j in range(len(out_map[i])):
            if out_map[i][j].isOrigin():
                origin_point = (i, j)
            if out_map[i][j].isExit():
                exit_point = (i, j)
    return (out_map, name, origin_point, exit_point)

# Class Jeu
class Jeu:
    def __init__(self, map):
        self.PERIODE: float | int = 0.25
        self.passed_time: float | int = 0
        self.grille: list[list[Case]] = map[0]
        self.map_name = map[1]
        self.origin_point = map[2]
        self.exit_point = map[3]
        self.lemmings: list[Lemming] = [Lemming(self.origin_point[0], self.origin_point[1])]
        self.score = 0
    
    def timing(self):
        if is_pressed('plus'):
            self.lemmings.append(Lemming(self.origin_point[0],self.origin_point[1]))
        copy_lem = []
        for i in self.lemmings:
            if (i.l, i.c) == self.exit_point:
                self.score += 1
                self.grille[i.l][i.c].liberer()
            else:
                copy_lem.append(i)
        self.lemmings = copy_lem.copy()
        for i in self.lemmings:
            i.tomber()
        if name == 'nt':
            system('cls')
        else:
            system('clear')
        print(self)
        self.passed_time = 0
    
    def demarrer(self):
        while not is_pressed('q'):
            sleep(self.PERIODE)
            self.timing()
        input('')
        return
    
    def __str__(self) -> str:
        out = ['\n'+self.map_name+'\n\n']
        for i in self.grille:
            for j in i:
                out.append(str(j))
            out.append('\n')
        out.append('\n\nScore: '+ str(self.score)+'\n')
        return ''.join(out)

game = None
maps = [map_loader(j) for j in ['./default_maps/' + i for i in listdir(path.abspath('./default_maps'))]]
names = '\n'.join([f'  {i}.' + maps[i][1] for i in range(len(maps))])

def main():
    status = True
    while status:
        try:
            map_wanted = int(input(f'\nWhich map?\n{names}\n> Your Choice: '))
            status = False
        except:
            pass
    current_map = maps[map_wanted]

    global game
    game = Jeu(current_map)

    if name == 'nt':
        system('cls')
    else:
        system('clear')

    game.demarrer()
    return

if __name__ == '__main__':
    main()
