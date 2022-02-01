###########
# WARNING: make sure to use python 3.10
###########

## Imports
# os for detect the os, clear the console window, and get all default maps
from os import name, system, listdir, path
# time to have a good framerate for the game and to respect the Jeu.PERIODE utilities mentionned in Lemmings.pdf
from time import sleep
# keyboard to detect key presses
from keyboard import is_pressed

###########
# WARNING: make sure to use python 3.10
###########

# Class Lemming
class Lemming:
    def __init__(self, origin_l: int, origin_c: int) -> None:
        self.l = origin_l # ligne, par défaut: ligne d'origine sur la map
        self.c = origin_c # colonne, par défaut: colonne d'origine sur la map
        self.d = 1 # 1 = droite, -1 = gauche
    
    def avancer(self):
        try: # Gère les erreurs
            if game.grille[self.l][self.c+self.d].estLibre() and not game.grille[self.l][self.c+self.d].estObstruee(): # Condition qui vérifie que la case dans la direction dans laquelle doit aller le lemmings est libre et non obstruee
                game.grille[self.l][self.c].liberer() # libere la case actuelle
                game.grille[self.l][self.c+self.d].occuper(self) # occupe la nouvelle case
                self.c += self.d # met a jour la colonne
            else:
                self.retourner() # sinon le lemmings se retourne
        except:
            self.retourner() # si erreur, fallback sur "le lemmings se retourne"
    
    def retourner(self):
        self.d *= -1 # retourne le lemmings

    def tomber(self):
        try: # Gère les erreurs
            if game.grille[self.l+1][self.c].estLibre() and not game.grille[self.l+1][self.c].estObstruee(): # Condition qui vérifie que la case dans laquelle doit tomber le lemmings est libre et non obstruee
                game.grille[self.l][self.c].liberer() # libere la case actuelle
                game.grille[self.l+1][self.c].occuper(self) # occupe la nouvelle case
                self.l += 1 # met a jour la ligne
            else:
                self.avancer() # sinon le lemmings avance
        except:
            self.avancer() # si erreur, fallback sur "le lemmings avance"
    
    def __str__(self) -> str:
        # Gère l'affichage du lemmings
        if self.d == 1:
            return '> '
        else:
            return '< '

###########
# WARNING: make sure to use python 3.10
###########

# Class Case
class Case:
    """The Case class"""
    def __init__(self, terrain: str = ' '):
        self.terrain: str = terrain # caractère représentant le terrain et donc si la case est obstruée ou non, #: obstruée, I: origine entrée, O: sortie
        self.lemming: Lemming = None
    
    def estLibre(self) -> bool:
        return self.lemming is None # vérifie l'absence de lemmings
    
    def estObstruee(self) -> bool:
        return self.terrain == '#' # vérifie si la case est obstruée
    
    def liberer(self):
        if not self.estObstruee() and not self.estLibre():
            self.lemming = None # libere la case après avoir vérifier que la case est occupée et est non obstruée
    
    def isOrigin(self) -> bool:
        return self.terrain == 'I' # vériie si c'est l'origine entrée
    
    def isExit(self) -> bool:
        return self.terrain == 'O' # vérifie si c'est la sortie
    
    def occuper(self, lemming: Lemming):
        if not self.estObstruee() and self.estLibre():
            self.lemming = lemming # occupe la case après avoir vérifier que la case n'est pas occupée et est non obstruée

    def __str__(self) -> str:
        # Gère l'affichage de la case
        if self.lemming is None:
            return self.terrain + " "
        else:
            return str(self.lemming)

###########
# WARNING: make sure to use python 3.10
###########

# Map Loader
def map_loader(path: str) -> tuple[list[list[Case]],str,tuple[int, int], tuple[int, int]]:
    # Charge une carte en chargeant sa grille, son nom et ses points d'entrée et de sortie
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

###########
# WARNING: make sure to use python 3.10
###########

# Class Jeu
class Jeu:
    def __init__(self, map):
        self.PERIODE: float | int = 0.225 # actualise le jeu tout les Jeu.PERIODE secondes
        self.grille: list[list[Case]] = map[0]
        self.map_name = map[1]
        self.origin_point = map[2]
        self.exit_point = map[3]
        self.lemmings: list[Lemming] = [Lemming(self.origin_point[0], self.origin_point[1])]
        self.score = 0
    
    def timing(self):
        if is_pressed('plus'): # gère le spawn des lemmings
            self.lemmings.append(Lemming(self.origin_point[0],self.origin_point[1]))
        # Calcul quels lemmings sont sortis
        copy_lem = []
        for i in self.lemmings:
            if (i.l, i.c) == self.exit_point:
                self.score += 1
                self.grille[i.l][i.c].liberer()
            else:
                copy_lem.append(i)
        self.lemmings = copy_lem.copy()
        for i in self.lemmings:
            i.tomber() # execute le comportement des lemmings: si peut tomber => tombe/ sinon => si peut avancer => avance/ sinon => se retourne
        # nettoie la console en detectant l'os pour ne pas se tromper de commande
        if name == 'nt':
            system('cls')
        else:
            system('clear')
        print(self) # affiche le jeu
    
    def demarrer(self):
        # fait tourner le jeu et le stop si "q" est pressé
        while not is_pressed('q'):
            sleep(self.PERIODE)
            self.timing()
        input('')
        return
    
    def __str__(self) -> str:
        # Gère l'affichage du jeu
        out = ['\n'+self.map_name+'\n\n']
        for i in self.grille:
            for j in i:
                out.append(str(j))
            out.append('\n')
        out.append('\n\nScore: '+ str(self.score)+'\n')
        return ''.join(out)

###########
# WARNING: make sure to use python 3.10
###########

game = None
# Charge les maps et leurs noms
maps = [map_loader(j) for j in ['./default_maps/' + i for i in listdir(path.abspath('./default_maps'))]]
names = '\n'.join([f'  {i}. ' + maps[i][1] for i in range(len(maps))])

def main():
    global maps
    global names
    global game
    # Prend le choix de map de l'utilisateur
    status = True
    while status:
        try:
            map_wanted = int(input(f'\nWhich map?\n{names}\n> Your Choice: '))
            if 0 <= map_wanted < len(names):
                status = False
        except:
            pass
    # Charge uniquement la map voulue et décharge les autres et leur noms
    current_map = maps[map_wanted]
    del maps
    del names

    # Lance le jeu
    game = Jeu(current_map)

    if name == 'nt':
        system('cls')
    else:
        system('clear')

    game.demarrer()
    return

###########
# WARNING: make sure to use python 3.10
###########

if __name__ == '__main__':
    main()

###########
# WARNING: make sure to use python 3.10
###########
