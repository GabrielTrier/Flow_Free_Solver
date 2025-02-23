import subprocess
from itertools import combinations

def build_dimacs_instance_n_queens(n):
    # Construction des variables
    # var_mapping[(i, j)] représente une reine à la position (i,j)
    var_mapping = {}
    var_counter = 1
    for i in range(n):
        for j in range(n):
            var_mapping[(i, j)] = var_counter
            var_counter += 1
    
    clauses = []
    
    # 1) Au moins une reine par ligne
    for i in range(n):
        clause = [var_mapping[(i, j)] for j in range(n)]
        clauses.append(clause)
        # Pas plus d'une reine par ligne
        for j1 in range(n):
            for j2 in range(j1 + 1, n):
                clauses.append([-var_mapping[(i, j1)], -var_mapping[(i, j2)]])
    
    # 2) Au moins une reine par colonne
    for j in range(n):
        clause = [var_mapping[(i, j)] for i in range(n)]
        clauses.append(clause)
        # Pas plus d'une reine par colonne
        for i1 in range(n):
            for i2 in range(i1 + 1, n):
                clauses.append([-var_mapping[(i1, j)], -var_mapping[(i2, j)]])
    
    # 3) Pas de reines sur la même diagonale
    # Diagonales principales
    for i in range(n):
        for j in range(n):
            # Diagonale descendante
            for k in range(1, n):
                if i + k < n and j + k < n:
                    clauses.append([-var_mapping[(i, j)], -var_mapping[(i + k, j + k)]])
            # Diagonale montante
            for k in range(1, n):
                if i + k < n and j - k >= 0:
                    clauses.append([-var_mapping[(i, j)], -var_mapping[(i + k, j - k)]])
    
    num_vars = var_counter - 1
    num_clauses = len(clauses)
    
    # Création du fichier DIMACS
    filename = "n_queens.cnf"
    with open(filename, "w") as f:
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    
    return filename, var_mapping

def solve_n_queens(n):
    cnf_filename, var_mapping = build_dimacs_instance_n_queens(n)
    try:
        result = subprocess.run(
            ["gophersat_win64.exe", cnf_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'appel à gophersat :", e.stderr)
        return {}
    
    queen_positions = {}
    for line in result.stdout.splitlines():
        if line.startswith("v"):
            parts = line.split()[1:]
            for lit in parts:
                lit_val = int(lit)
                if lit_val > 0:
                    for (i, j), var in var_mapping.items():
                        if var == lit_val:
                            queen_positions[(i, j)] = 1
                            break
    return queen_positions