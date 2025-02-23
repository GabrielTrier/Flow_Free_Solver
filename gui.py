from tkinter import messagebox
import tkinter as tk
from solveur_queen import solve_n_queens

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Solver")
        self.root.configure(bg="black")  # Fond noir de l'application
        self.n = 4  # Taille initiale
        self.cell_size = 60
        
        # Frame pour les contrôles
        self.control_frame = tk.Frame(root, bg="black")
        self.control_frame.pack(pady=10)
        
        # Boutons pour modifier la taille
        self.decrease_btn = tk.Button(self.control_frame, text="-", command=self.decrease_size, 
                                      bg="gray20", fg="white", font=("Helvetica", 16, "bold"))
        self.decrease_btn.pack(side=tk.LEFT, padx=5)
        
        self.size_label = tk.Label(self.control_frame, text=f"Taille: {self.n}", bg="gray20", fg="white", 
                                   font=("Helvetica", 22, "bold"), padx=20)
        self.size_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.increase_btn = tk.Button(self.control_frame, text="+", command=self.increase_size, 
                                      bg="gray20", fg="white", font=("Helvetica", 16, "bold"))
        self.increase_btn.pack(side=tk.LEFT, padx=5)
        
        self.solve_btn = tk.Button(self.control_frame, text="Résoudre", command=self.solve_puzzle, 
                                   bg="gray20", fg="white", font=("Helvetica", 16, "bold"))
        self.solve_btn.pack(side=tk.LEFT, padx=20)
        
        # Canvas pour l'échiquier
        self.canvas_size = self.n * self.cell_size
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="black", highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)
        
        self.draw_board()
    
    def draw_board(self):
        self.canvas.delete("all")
        self.canvas_size = self.n * self.cell_size
        self.canvas.config(width=self.canvas_size, height=self.canvas_size, bg="black")
        
        # Dessiner l'échiquier avec des bordures bien définies
        for i in range(self.n):
            for j in range(self.n):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="white", width=2)
    
    def draw_queens(self, positions):
        queen_image = "♕"  # Caractère Unicode pour la reine
        for (i, j), k in positions.items():
            x = j * self.cell_size + self.cell_size // 2
            y = i * self.cell_size + self.cell_size // 2
            self.canvas.create_text(x, y, text=queen_image, font=("Arial", int(self.cell_size * 0.6), "bold"), fill="yellow")
    
    def increase_size(self):
        if self.n < 15:  # Limite maximale
            self.n += 1
            self.size_label.config(text=f"Taille: {self.n}")
            self.draw_board()
    
    def decrease_size(self):
        if self.n > 4:  # Limite minimale pas de solution pour n < 4 
            self.n -= 1
            self.size_label.config(text=f"Taille: {self.n}")
            self.draw_board()
    
    def solve_puzzle(self):
        try:
            positions = solve_n_queens(self.n)
            if positions:
                self.draw_board()
                self.draw_queens(positions)
            else:
                messagebox.showerror("Erreur", "Aucune solution trouvée")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {str(e)}")

def launch_gui():
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
