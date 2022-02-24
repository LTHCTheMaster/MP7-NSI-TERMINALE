###########
# WARNING: make sure to use python 3.10
###########

## Imports
# os for detect the os, clear the console window, and get all default maps
from os import name, system, listdir, path
# time to have a good framerate for the game and to respect the Jeu.PERIODE utilities mentionned in Lemmings.pdf
from time import sleep, time
# keyboard to detect key presses
from keyboard import is_pressed
# datetime to indicates time in logs
from datetime import datetime

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
                logger.write_log('Lemming: avancer()')
            else:
                self.retourner() # sinon le lemmings se retourne
                logger.write_log('Lemming: avancer -> nope -> goto retourner')
        except:
            self.retourner() # si erreur, fallback sur "le lemmings se retourne"
            logger.write_log('Lemming: avancer -> error -> goto retourner')
    
    def retourner(self):
        self.d *= -1 # retourne le lemmings
        logger.write_log('Lemming: retourner()')

    def tomber(self):
        try: # Gère les erreurs
            if game.grille[self.l+1][self.c].estLibre() and not game.grille[self.l+1][self.c].estObstruee(): # Condition qui vérifie que la case dans laquelle doit tomber le lemmings est libre et non obstruee
                game.grille[self.l][self.c].liberer() # libere la case actuelle
                game.grille[self.l+1][self.c].occuper(self) # occupe la nouvelle case
                self.l += 1 # met a jour la ligne
                logger.write_log('Lemming: tomber()')
            else:
                self.avancer() # sinon le lemmings avance
                logger.write_log('Lemming: tomber -> nope -> goto avancer')
        except:
            self.avancer() # si erreur, fallback sur "le lemmings avance"
            logger.write_log('Lemming: tomber -> error -> goto avancer')
    
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

# Class Logger_builder
class Logger_builder:
    def __init__(self):
        log_path = './logs.log'
        if not path.exists(path.abspath(log_path)):
            self.file = open(path.abspath(log_path),'w')
        else:
            self.file = open(path.abspath(log_path),'r')
            content = self.file.read()
            self.close()
            if content.count('New Logs at') >= 3:
                self.file = open(path.abspath(log_path), 'w')
            else:
                self.file = open(path.abspath(log_path), 'a')
            del content

        self.file.write(f'New Logs at {datetime.fromtimestamp(time())}:\n')
    
    def write_log(self, message):
        self.file.write(f'    {message}\n')
    
    def close(self):
        self.file.close()

# Class Map_loaded
class Map_loaded:
    def __init__(self, path: str):
        # Charge une carte en chargeant sa grille, son nom et ses points d'entrée et de sortie
        self.out_map: list[list[Case]] = []
        file = open(path, 'r+')
        file.write('')
        self.name = file.readline()[9:].replace('\n','')
        map_raw = file.readlines()
        for i in map_raw:
            add = []
            for j in i.replace('\n',''):
                add.append(Case(j))
            self.out_map.append(add.copy())
        self.origin_point = None
        self.exit_point = None
        for i in range(len(self.out_map)):
            for j in range(len(self.out_map[i])):
                if self.out_map[i][j].isOrigin():
                    self.origin_point = (i, j)
                if self.out_map[i][j].isExit():
                    self.exit_point = (i, j)
        if self.origin_point is None or self.exit_point is None:
            raise Exception("The map must have origin point and exit point")

###########
# WARNING: make sure to use python 3.10
###########

# Class Jeu
class Jeu:
    def __init__(self, map: Map_loaded):
        self.PERIODE: float | int = 0.225 # actualise le jeu tout les Jeu.PERIODE secondes
        self.grille: list[list[Case]] = map.out_map
        self.map_name = map.name
        self.origin_point = map.origin_point
        self.exit_point = map.exit_point
        self.lemmings: list[Lemming] = [Lemming(self.origin_point[0], self.origin_point[1])]
        self.score = 0
    
    def timing(self):
        if is_pressed('plus'): # gère le spawn des lemmings
            self.lemmings.append(Lemming(self.origin_point[0],self.origin_point[1]))
            logger.write_log('Jeu: summon a new Lemming')
        # Calcul quels lemmings sont sortis
        copy_lem = []
        counter_of_lemmings = 0
        for i in self.lemmings:
            if (i.l, i.c) == self.exit_point:
                self.score += 1
                self.grille[i.l][i.c].liberer()
                logger.write_log(f'Jeu: Lemming {counter_of_lemmings} exit')
            else:
                copy_lem.append(i)
                logger.write_log(f'Jeu: Lemming {counter_of_lemmings} don\'t exit')
            counter_of_lemmings += 1
        self.lemmings = copy_lem.copy()
        counter_of_lemmings = 0
        for i in self.lemmings:
            logger.write_log(f'Jeu: Lemming {counter_of_lemmings} action follow')
            i.tomber() # execute le comportement des lemmings: si peut tomber => tombe/ sinon => si peut avancer => avance/ sinon => se retourne
            counter_of_lemmings += 1
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
        logger.write_log('ENDING REQUIRED')
        input('')
        logger.write_log('ENDING ACCEPTED')
        return
    
    def __str__(self) -> str:
        # Gère l'affichage du jeu
        out = ['\n'+self.map_name+'\n\n']
        for i in self.grille:
            for j in i:
                out.append(str(j))
            out.append('\n')
        out.append('\n\nScore: '+ str(self.score)+'\n')
        logger.write_log('Jeu: Excute a Display')
        return ''.join(out)

###########
# WARNING: make sure to use python 3.10
###########

game = None
logger = None
# Charge les maps et leurs noms
maps = [Map_loaded(j) for j in ['./default_maps/' + i for i in listdir(path.abspath('./default_maps'))]]
names = '\n'.join([f'  {i}. ' + maps[i].name for i in range(len(maps))])

def main():
    global maps
    global names
    global game
    global logger
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
    logger = Logger_builder()
    logger.write_log(f'INIT SEQUENCE: {map_wanted} choosen')
    del maps
    del names

    # Lance le jeu
    game = Jeu(current_map)

    if name == 'nt':
        system('cls')
    else:
        system('clear')

    game.demarrer()

    logger.write_log(f'ENDING SEQUENCE: Game Ended with a score of {game.score}')
    logger.close()
    return

###########
# WARNING: make sure to use python 3.10
###########

if __name__ == '__main__':
    main()

###########
# WARNING: make sure to use python 3.10
###########
