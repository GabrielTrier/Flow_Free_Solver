import tkinter as tk

# A modifier pour améliorer les affichages!!!
# On peut sauvegarder les solutions???  faire un avant/après ?? I
# interface en ligne
def display_solution(puzzle, edge_solution):
    dim = puzzle.dim
    cell_size = 80
    margin = 40
    canvas_size = cell_size * dim + 2 * margin

    def cell_center(i, j):
        x = margin + j * cell_size + cell_size/2
        y = margin + i * cell_size + cell_size/2
        return x, y

    fen = tk.Tk()
    fen.title("Flow Free - Solution")
    canvas = tk.Canvas(fen, width=canvas_size, height=canvas_size, bg="white")
    canvas.pack()

    #Tracer la grille
    for i in range(dim + 1):
        y = margin + i * cell_size
        canvas.create_line(margin, y, margin + dim * cell_size, y, fill="black")
    for j in range(dim + 1):
        x = margin + j * cell_size
        canvas.create_line(x, margin, x, margin + dim * cell_size, fill="black")

    #Tracer les arêtes utilisées
    for e, color in edge_solution.items():
        (i1, j1), (i2, j2) = e
        x1, y1 = cell_center(i1, j1)
        x2, y2 = cell_center(i2, j2)
        canvas.create_line(x1, y1, x2, y2, fill=color, width=12, capstyle=tk.ROUND)

    #Marquer les terminaux par des cercles
    rayon = cell_size * 0.15
    for v, color in puzzle.terminals.items():
        i, j = v
        x, y = cell_center(i, j)
        canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon,
                           fill=color, outline="black", width=2)
    
    canvas.create_text(canvas_size/2, margin/2, text="Flow Free - Solution", font=("Helvetica", 16))
    fen.mainloop()
