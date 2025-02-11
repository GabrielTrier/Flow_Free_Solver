import importlib.util
import sys
from puzzle import Puzzle
from sat_solver import build_sat_instance
from display import display_solution

def load_puzzle_config(path):
    spec = importlib.util.spec_from_file_location("puzzle_config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.puzzle_config

def main():
    config_path = sys.argv[1]
    config = load_puzzle_config(config_path)
    puzzle = Puzzle.from_config(config)
    
    solver, edge_vars, edges = build_sat_instance(puzzle)
    if solver.solve():
        model = solver.get_model() #Retourne les variables qui sont vraies
        edge_solution = {}
        allowed_colors = sorted(set(puzzle.terminals.values()))

        #Extraire les couleurs assignées aux arêtes
        for e in edges:
            assigned_color = None
            for color in allowed_colors:
                if edge_vars[(e, color)] in model:
                    assigned_color = color
                    break
            if assigned_color is not None:
                edge_solution[e] = assigned_color
        solver.delete() #Libérer la mémoire
        display_solution(puzzle, edge_solution)
    else:
        print("Aucune solution trouvée pour ce puzzle!")
        solver.delete()

if __name__ == "__main__":
    main()
