"""
Le fichier puzzle.py contient la définition de la classe Puzzle afin de représenter un puzzle de type "Flow Free".
Un puzzle est défini par sa dimension (dim) et un ensemble de terminaux.
Un terminal est une case de la grille qui doit être reliée à un autre terminal de même couleur!
Cela nous permet de charger directement une configuration de "puzzle" depuis un fichier Python, représnetant donc un niveau d ejeu que le solver doit résoudre!
"""
class Puzzle:
    def __init__(self, dim, terminals):
        self.dim = dim  #Dimension de la grille (dim x dim)
        self.terminals = terminals  #Dictionnaire : (i, j) -> couleur (string)
        self.nodes = [(i, j) for i in range(dim) for j in range(dim)]
    
    @classmethod
    def from_config(cls, config):
        """
        La configuration est un dictionnaire avec les clés :
          - "dim": dimension (int)
          - "nodes": liste d'assignations sous la forme [[i, j], {"color": couleur}]
        """
        dim = config["dim"]
        terminals = {}
        for entry in config["nodes"]:
            coord = tuple(entry[0])
            info = entry[1]
            color = info["color"]
            terminals[coord] = color
        return cls(dim, terminals)
