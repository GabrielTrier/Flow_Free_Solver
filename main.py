import tkinter as tk
import importlib.util
from puzzle import Puzzle
from sat_solver import build_sat_instance
import display
from display import save_solution_image
from gophersat_solver import solve_with_gophersat
from gui import launch_gui
import os
import subprocess

#Variables globales
current_puzzle = None
current_level = None
current_canvas = None

#Frames pour la gestion des pages
home_frame = None
puzzle_frame = None

######################GopherSAT######################

def solve_with_gophersat_interface():
    """
    Utilise Gophersat pour résoudre le puzzle courant et met à jour l'affichage.
    """
    global current_puzzle, current_canvas
    if current_puzzle is None:
        return
    edge_solution = solve_with_gophersat(current_puzzle)
    if edge_solution:
        draw_solution(current_canvas, current_puzzle, edge_solution)
    else:
        print("Aucune solution trouvée avec Gophersat.")

######################Affichage et SAT######################

def load_puzzle_config(path):
    spec = importlib.util.spec_from_file_location("puzzle_config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.puzzle_config

def draw_initial_puzzle(canvas, puzzle):
    """
    Affiche la configuration initiale du puzzle sur le canvas Tkinter
    """
    canvas.delete("all")
    dim = puzzle.dim
    new_width = display.CELL_SIZE * dim + 2 * display.MARGIN
    new_height = display.CELL_SIZE * dim + 2 * display.MARGIN
    canvas.config(width=new_width, height=new_height)

    #Dessine la grille
    for i in range(dim + 1):
        y = display.MARGIN + i * display.CELL_SIZE
        canvas.create_line(display.MARGIN, y, display.MARGIN + dim * display.CELL_SIZE, y,
                           fill="white", tags="grid")
    for j in range(dim + 1):
        x = display.MARGIN + j * display.CELL_SIZE
        canvas.create_line(x, display.MARGIN, x, display.MARGIN + dim * display.CELL_SIZE,
                           fill="white", tags="grid")
    #Dessine les terminaux
    rayon = display.CELL_SIZE * 0.15
    for (i, j), color in puzzle.terminals.items():
        x = display.MARGIN + j * display.CELL_SIZE + display.CELL_SIZE/2
        y = display.MARGIN + i * display.CELL_SIZE + display.CELL_SIZE/2
        canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon,
                           fill=color, outline="white", width=2, tags="terminals")
    #Titre
    canvas.create_text(new_width/2, display.MARGIN/2, text="Flow Free - Puzzle Initial",fill="yellow", font=("Helvetica", 16, "bold"), tags="title")

def draw_solution(canvas, puzzle, edge_solution):
    for e, color in edge_solution.items():
        (i1, j1), (i2, j2) = e
        x1 = display.MARGIN + j1 * display.CELL_SIZE + display.CELL_SIZE/2
        y1 = display.MARGIN + i1 * display.CELL_SIZE + display.CELL_SIZE/2
        x2 = display.MARGIN + j2 * display.CELL_SIZE + display.CELL_SIZE/2
        y2 = display.MARGIN + i2 * display.CELL_SIZE + display.CELL_SIZE/2
        canvas.create_line(x1, y1, x2, y2, fill=color, width=12,capstyle=tk.ROUND, tags="solution")

    dim = puzzle.dim
    canvas_width = display.CELL_SIZE * dim + 2 * display.MARGIN
    canvas.itemconfig("title", text="Flow Free - Puzzle Solved")

def compute_edge_solution(puzzle):
    """
    Calcule et renvoie le dictionnaire edge_solution pour le puzzle courant.
    """
    solver, edge_vars, edges = build_sat_instance(puzzle)#Appel de la fonction build_sat_instance (voir sat_solver.py)
    edge_solution = {}
    if solver.solve():
        model = solver.get_model()#Retourne les variables qui sont vraies
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
    else:
        print("Aucune solution trouvée pour ce puzzle!")
    solver.delete()#Libérer la mémoire
    return edge_solution

#Fonction pour mettre à jour l'affichage de la solution
def solve_current_puzzle():
    global current_puzzle, current_canvas
    if current_puzzle is None:
        return
    edge_solution = compute_edge_solution(current_puzzle)
    if edge_solution:
        draw_solution(current_canvas, current_puzzle, edge_solution)

#Appel de la fonction save_solution_image de display.py pour sauvegarder la solution
def save_solution():
    global current_puzzle, current_level
    if current_puzzle is None or current_level is None:
        return
    edge_solution = compute_edge_solution(current_puzzle)
    if edge_solution:
        from display import save_solution_image
        save_solution_image(current_puzzle, edge_solution, current_level)
    else:
        print("Impossible de sauvegarder la solution pour ce puzzle!")

############################################Fonction Gestion MENU Tkinter############################################
def return_to_home():
    global home_frame, puzzle_frame
    puzzle_frame.pack_forget()
    home_frame.pack(fill=tk.BOTH, expand=True)

def select_level(level):
    global current_puzzle, current_level, home_frame, puzzle_frame, current_canvas
    current_level = level
    config_path = f"puzzles/puzzle{level}.py"

    config = load_puzzle_config(config_path)#Charge la configuration du puzzle
    current_puzzle = Puzzle.from_config(config)#Appel de la méthode from_config de la classe Puzzle
    home_frame.pack_forget()
    puzzle_frame.pack(fill=tk.BOTH, expand=True)
    draw_initial_puzzle(current_canvas, current_puzzle)

def create_home_interface(root):
    home = tk.Frame(root, bg="black")
    title = tk.Label(home, text="Connecting Dots", bg="black",fg="yellow", font=("Helvetica", 48, "bold"))
    title.pack(pady=80)
    
    levels_frame = tk.Frame(home, bg="black")
    levels_frame.pack()
    
    level = 1
    for row in range(2):
        for col in range(2):
            btn = tk.Label(levels_frame, text=f"Niveau {level}", bg="black",
                           fg="white", font=("Helvetica", 24, "underline"), cursor="hand2")
            btn.grid(row=row, column=col, padx=30, pady=30)
            btn.bind("<Button-1>", lambda e, lvl=level: select_level(lvl))
            level += 1
            if level > 4:
                break
        if level > 4:
            break
    return home

def create_puzzle_interface(root):
    """
    Crée l'interface du puzzle avec une barre en haut contenant les boutons "Back", "Solve" et "Save Solution", et un canvas centré.
    """
    global current_canvas
    frame = tk.Frame(root, bg="black")
    
    #Barre en haut
    top_bar = tk.Frame(frame, bg="black")
    top_bar.pack(fill=tk.X, pady=10)
    back_btn = tk.Button(top_bar, text="← Back", bg="gray20", fg="white",
                         font=("Helvetica", 14, "bold"), command=return_to_home)
    back_btn.pack(side=tk.LEFT, padx=20)
    solve_btn = tk.Button(top_bar, text="Solve (SAT)", bg="gray20", fg="white",
                          font=("Helvetica", 16, "bold"), command=solve_current_puzzle)
    solve_btn.pack(side=tk.LEFT, padx=20)
    gupher_btn = tk.Button(
        top_bar,
        text="Solve (Gophersat)",
        bg="gray20",
        fg="white",
        font=("Helvetica", 16, "bold"),
        command=solve_with_gophersat_interface,
    )
    gupher_btn.pack(side=tk.LEFT, padx=20)
    save_btn = tk.Button(top_bar, text="Save Solution", bg="gray20", fg="white",
                         font=("Helvetica", 16, "bold"), command=save_solution)
    save_btn.pack(side=tk.LEFT, padx=20)
    
    #Cadre pour centrer le canvas
    canvas_frame = tk.Frame(frame, bg="black")
    canvas_frame.pack(expand=True)
    current_canvas = tk.Canvas(canvas_frame, bg="black")
    current_canvas.pack(expand=True)
    
    return frame

def create_main_interface_flow_free():
    root = tk.Tk()
    root.title("Flow Free Solver")
    root.configure(bg="black")
    root.geometry("1200x800")
    
    global home_frame, puzzle_frame
    home_frame = create_home_interface(root)
    home_frame.pack(fill=tk.BOTH, expand=True)
    
    puzzle_frame = create_puzzle_interface(root)
    puzzle_frame.pack_forget()
    
    return root

def create_main_interface_n_queens():
    #fonction launchgui de test_queens
    launch_gui()

def open_pdf_Linux():
    pdf_path = "Bouaita_Trier_Rapport.pdf"
    if os.path.exists(pdf_path):
        subprocess.run(["xdg-open", pdf_path], check=True)  
    else:
        print("Le fichier PDF n'existe pas.")

def open_pdf_Windows():
    pdf_path = "Bouaita_Trier_Rapport.pdf"
    if os.path.exists(pdf_path):
        subprocess.run(["start", "", pdf_path], shell=True, check=True) 
    else:
        print("Le fichier PDF n'existe pas.")

def open_pdf_MacOS():
    pdf_path = "Bouaita_Trier_Rapport.pdf"
    if os.path.exists(pdf_path):
        subprocess.run(["open", pdf_path], check=True) 
    else:
        print("Le fichier PDF n'existe pas.")

def create_main_interface():
    root = tk.Tk()
    root.title("Choix du jeu")
    root.geometry("400x350")
    root.configure(bg="black")

    frame = tk.Frame(root, bg="black")
    frame.pack(expand=True)

    queens_btn = tk.Button(frame, text="N-Queens", bg="gray20", fg="white",
                           font=("Helvetica", 16, "bold"), command=create_main_interface_n_queens)
    queens_btn.pack(pady=10)
    
    flow_free_btn = tk.Button(frame, text="Flow Free", bg="gray20", fg="white",
                              font=("Helvetica", 16, "bold"), command=create_main_interface_flow_free)
    flow_free_btn.pack(pady=10)
    open_pdf_btn_linux = tk.Button(frame, text="Ouvrir le rapport (Linux)", bg="red", fg="white",
                                   font=("Helvetica", 16, "bold"), command=open_pdf_Linux)
    open_pdf_btn_linux.pack(pady=10)


    open_pdf_btn_windows = tk.Button(frame, text="Ouvrir le rapport (Windows)", bg="red", fg="white",
                                     font=("Helvetica", 16, "bold"), command=open_pdf_Windows)
    open_pdf_btn_windows.pack(pady=10)

    open_pdf_btn_macos = tk.Button(frame, text="Ouvrir le rapport (MacOS)", bg="red", fg="white",
                                  font=("Helvetica", 16, "bold"), command=open_pdf_MacOS)
    open_pdf_btn_macos.pack(pady=10)

    return root

if __name__ == "__main__":
    root = create_main_interface()
    root.mainloop()