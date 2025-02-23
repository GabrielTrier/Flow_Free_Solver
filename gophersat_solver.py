import os
import subprocess
from itertools import combinations

def build_dimacs_instance(puzzle):
    dim = puzzle.dim
    terminals = puzzle.terminals
    allowed_colors = sorted(set(terminals.values()))
    
    # Construction du graphe
    edges = []
    for i in range(dim):
        for j in range(dim):
            if j + 1 < dim:
                edges.append(((i, j), (i, j + 1)))
            if i + 1 < dim:
                edges.append(((i, j), (i + 1, j)))
    
    var_mapping = {}
    var_counter = 1
    for e in edges:
        for c in allowed_colors:
            var_mapping[(e, c)] = var_counter
            var_counter += 1
    
    clauses = []

    # Contrainte : arête au plus 1 couleur
    for e in edges:
        for c1, c2 in combinations(allowed_colors, 2):
            clauses.append([-var_mapping[(e, c1)], -var_mapping[(e, c2)]])

    # Fonction utilitaire
    def incident_edges(v):
        return [e for e in edges if v in e]

    for v in puzzle.nodes:
        inc = incident_edges(v)
        if v not in terminals:
            # EXACTEMENT 2 ARÊTES
            # 1) Au plus 2 : pour chaque triplet, pas toutes vraies.
            vars_all = [var_mapping[(e, c)] for e in inc for c in allowed_colors]
            for subset in combinations(vars_all, 3):
                clauses.append([-lit for lit in subset])

            # 2) Au moins 2 : pour toute sous-famille de taille (len(vars_all) - 2 + 1),
            n = len(vars_all)
            for subset in combinations(vars_all, n - 2 + 1):
                clauses.append(list(subset))

            # UNIFORMITÉ DE COULEUR
            for e1, e2 in combinations(inc, 2):
                for c1 in allowed_colors:
                    for c2 in allowed_colors:
                        if c1 != c2:
                            clauses.append(
                                [-var_mapping[(e1, c1)], -var_mapping[(e2, c2)]]
                            )
        else:
            # Noeud terminal
            term_color = terminals[v]
            inc_vars = []
            for e in inc:
                for c in allowed_colors:
                    if c != term_color:
                        clauses.append([-var_mapping[(e, c)]])
                inc_vars.append(var_mapping[(e, term_color)])
            
            # EXACTEMENT 1 pour le terminal => "au plus 1" + "au moins 1"
            for v1, v2 in combinations(inc_vars, 2):
                clauses.append([-v1, -v2])
            clauses.append(inc_vars)

    num_vars = var_counter - 1
    num_clauses = len(clauses)
    
    # Création du fichier DIMACS
    filename = "flow_free.cnf"
    with open(filename, "w") as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

    return filename, var_mapping


def solve_with_gophersat(puzzle):
    cnf_filename, var_mapping = build_dimacs_instance(puzzle)

    try:
        result = subprocess.run(
            [r"gophersat_win64.exe", cnf_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'appel à gophersat :", e.stderr)
        return {}

    edge_solution = {}
    for line in result.stdout.splitlines():
        if line.startswith("v"):
            parts = line.split()[1:]
            for lit in parts:
                lit_val = int(lit)
                if lit_val > 0:
                    for (e, c), var in var_mapping.items():
                        if var == lit_val:
                            edge_solution[e] = c
                            break
    return edge_solution