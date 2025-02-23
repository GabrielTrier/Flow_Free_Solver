import os
from PIL import Image, ImageDraw, ImageFont

#Constantes d'affichage (adaptable)
CELL_SIZE = 80
MARGIN = 40

#Listes de fonctions utilitaires pour l'affichage des grilles et des solutions mais surtout pour la sauvegarde!
def cell_center(i, j):
    x = MARGIN + j * CELL_SIZE + CELL_SIZE / 2
    y = MARGIN + i * CELL_SIZE + CELL_SIZE / 2
    return x, y

def draw_grid_on_image(draw, dim):
    canvas_width = CELL_SIZE * dim + 2 * MARGIN
    #Lignes horizontales
    for i in range(dim + 1):
        y = MARGIN + i * CELL_SIZE
        draw.line((MARGIN, y, MARGIN + dim * CELL_SIZE, y), fill="white")
    #Lignes verticales
    for j in range(dim + 1):
        x = MARGIN + j * CELL_SIZE
        draw.line((x, MARGIN, x, MARGIN + dim * CELL_SIZE), fill="white")

def draw_terminals_on_image(draw, puzzle):
    rayon = CELL_SIZE * 0.15
    for (i, j), color in puzzle.terminals.items():
        x, y = cell_center(i, j)
        bbox = (x - rayon, y - rayon, x + rayon, y + rayon)
        draw.ellipse(bbox, fill=color, outline="white", width=2)

def draw_solution_on_image(draw, puzzle, edge_solution):
    """Dessine les arêtes de solution sur l'image."""
    for e, color in edge_solution.items():
        (i1, j1), (i2, j2) = e
        x1, y1 = cell_center(i1, j1)
        x2, y2 = cell_center(i2, j2)
        draw.line((x1, y1, x2, y2), fill=color, width=12)

def save_solution_image(puzzle, edge_solution, level):
    dim = puzzle.dim
    new_width = CELL_SIZE * dim + 2 * MARGIN
    new_height = CELL_SIZE * dim + 2 * MARGIN
    img = Image.new("RGB", (new_width, new_height), "black")
    draw = ImageDraw.Draw(img)

    #Dessiner grille, terminaux et solution
    draw_grid_on_image(draw, dim)
    draw_terminals_on_image(draw, puzzle)
    draw_solution_on_image(draw, puzzle, edge_solution)

    title_text = "Flow Free - Puzzle Solved"
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    #Utilisation de textbbox si disponible, sinon fallback sur font.getsize
    try:
        bbox = draw.textbbox((0, 0), title_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = font.getsize(title_text)
    title_position = ((new_width - text_width) / 2, MARGIN/2 - text_height/2)
    draw.text(title_position, title_text, fill="yellow", font=font)

    #Sauvegarde de l'image
    if not os.path.exists("solutions"):
        os.makedirs("solutions")
    filename = f"solutions/solution_level{level}.png"
    img.save(filename, "PNG")
    print("Solution sauvegardée dans", filename)

