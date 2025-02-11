from itertools import combinations
from pysat.solvers import Glucose3

def add_exactly_k(solver, vars_list, k):
    n = len(vars_list)
    #Au moins k vraies
    for subset in combinations(vars_list, n - k + 1):
        solver.add_clause(list(subset))
    #Au plus k vraies
    for subset in combinations(vars_list, k + 1):
        solver.add_clause([-v for v in subset])

def add_exactly_one(solver, vars_list):
    add_exactly_k(solver, vars_list, 1)

def connected_edges(v):
        return [e for e in edges if v in e]
    
def build_sat_instance(puzzle):
    """
    Construit l'instance SAT pour un Puzzle.
    Retourne (solver, edge_vars, edges) où :
      - solver: l'instance du solveur SAT avec les contraintes ajoutées.
      - edge_vars: dictionnaire qui associe à (edge, couleur) un identifiant SAT.
      - edges: liste des arêtes du graphe.
    """
    dim = puzzle.dim
    nodes = puzzle.nodes
    terminals = puzzle.terminals
    allowed_colors = sorted(set(terminals.values())) #Couleurs autorisés sont celles des terminaux du puzzle afin d'etre adaptable pour differents puzzles
    
    #Construction du graphe 
    #Chaque cellule (i,j) est un noeud et une arête relie deux cellules adjacentes (voisinage de 4)
    edges = []
    for i in range(dim):
        for j in range(dim):
            if j + 1 < dim:
                edges.append(((i, j), (i, j+1)))
            if i + 1 < dim:
                edges.append(((i, j), (i+1, j)))
    
    #Création des variables SAT pour chaque arête et pour chaque couleur
    edge_vars = {}
    var_counter = 1
    for e in edges:
        for color in allowed_colors:
            edge_vars[(e, color)] = var_counter
            var_counter += 1

    solver = Glucose3()
    
    #Contrainte 1 : Chaque arête porte au plus une couleur: ¬x(e,c1​) ∨ ¬x(e,c2​)
    for e in edges:
        for c1, c2 in combinations(allowed_colors, 2):
            solver.add_clause([-edge_vars[(e, c1)], -edge_vars[(e, c2)]])
    
    #Contraintes 2 sur les nœuds
    for v in nodes:
        inc_edges = connected_edges(v)
        if v not in terminals:
            #Si Noeud non terminal --> il doit être traversé par exactement 2 arêtes (toutes couleurs confondues)
            vars_all = [edge_vars[(e, color)] for e in inc_edges for color in allowed_colors]
            add_exactly_k(solver, vars_all, 2)
            #Les 2 arêtes doivent être de même couleur
            for e1, e2 in combinations(inc_edges, 2):
                for c1 in allowed_colors:
                    for c2 in allowed_colors:
                        if c1 != c2:
                            solver.add_clause([-edge_vars[(e1, c1)], -edge_vars[(e2, c2)]])
        else:
            #Si Noeud terminal -> il doit avoir une unique couleur (qui est celle fixé)
            term_color = terminals[v]
            #Pour chaque arête incidente on interdit toute couleur différente de term_color
            for e in inc_edges:
                for c in allowed_colors:
                    if c != term_color:
                        solver.add_clause([-edge_vars[(e, c)]])
            #Exactement 1 arête active parmi les arêtes incidentes: x(e,term_color) 
            vars_term = [edge_vars[(e, term_color)] for e in inc_edges]
            add_exactly_one(solver, vars_term) #Assurer qu'une est vraie
    
    return solver, edge_vars, edges
