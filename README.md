# **Connaissance et Raisonnement**
## **Projet : Résolution de puzzles à l’aide de solveurs SAT**

## **Abstract**

Ce projet présente la résolution de deux puzzles, Flow Free et n-queens, en utilisant une
réduction en SAT. Nous expliquons la modélisation du problème sous forme de clauses CNF et
la résolution à l’aide d’un solveur SAT. L’objectif est de démontrer comment un problème de
satisfaction de contraintes peut être converti en une instance SAT et résolu efficacement.

Le projet est organisé de manière modulaire avec plusieurs fichiers :

- **`puzzle.py`**  
  Définit la classe **`Puzzle`** qui représente un puzzle en termes de dimension de la grille et d’assignation des nœuds terminaux (leur position et leur couleur).

- **`sat_solver.py`**  
  Construit l’instance SAT (pour Flow Free) en traduisant les contraintes du puzzle en clauses CNF et en associant une variable \( x(e, c) \) pour chaque arête **e** et chaque couleur **c**. 

- **`display.py`**  
  Contient les fonctions de dessin et de sauvegarde d’images de la grille, des terminaux et de la solution à l’aide de Pillow.

- **`main.py`**  
  Gère l’interface graphique (via Tkinter), la navigation entre la page d’accueil et l’interface du puzzle, ainsi que la résolution et la sauvegarde des solutions.

- **`puzzles/`**  
  Ce dossier contient plusieurs fichiers de configuration (par exemple, `puzzle1.py`, `puzzle2.py`, etc.) qui définissent des puzzles sous la forme de dictionnaires.

- **`solutions/`**  
  Ce dossier contient les solutions des différents niveaux qui sont les différents puzzles.

- **`solveur_queen.py`**
  Contient la modélisation du problème des n-queens en SAT et la résolution du problème.

- **`gui.py`**
  Contient la classe **`GUI`** qui gère l'interface graphique du problème n-queens.


## **Installation et Exécution**

### **Prérequis**

- **Python 3.x**
- **Bibliothèque `python-sat`** pour le solveur SAT ainsi que `Pillow`
- **Tkinter** pour l'affichage graphique (généralement inclus avec Python)

### **Installation des Dépendances**

Exécutez la commande suivante pour installer les dépendances:

```bash
pip install python-sat
pip install Pillow
```
### **Execution**

1. Cloner le projet ou télécharger les fichiers dans un répertoire local.
2. Lancer le programme en exécutant :
```bash
python main.py
```
3. 5 boutons sont disponibles :
- **`Flow Free`** : Résolution du puzzle Flow Free/Conencting dots avec 4 niveaux.
- **`N-Queens`** : Résolution du problème des n-queens.
- **`Ouvrir le rapport pour Linux`** : Ouvrir le rapport du projet.
- **`Ouvrir le rapport pour Windows`** : Ouvrir le rapport du projet.
- **`Ouvrir le rapport pour MacOS`** : Ouvrir le rapport du projet.


4. Pour Flow Free naviguer à travers les différnets niveaux :
- Une page d’accueil s'affiche avec le titre "Connecting Dots" et une grille (2x2) pour choisir le niveau (1 à 4)
- Cliquez sur le niveau souhaité pour charger le puzzle correspondant
- Dans l'interface du puzzle:
    - Cliquez sur Back pour revenir ua menu principal
    - Cliquez sur Solve pour résoudre le puzzle et afficher la solution
    - Cliquez sur Save Solution pour sauvegarder l’image de la solution
    
5. Pour N-Queens :
- Une page d’accueil s'affiche avec le titre "N-Queens" et une grille (4x4) pour choisir le nombre de reines (4 à 15)
- Augmentez le nombre de reines avec les boutons "+" et "-" pour charger le puzzle correspondant. 
- Résoudre le puzzle en cliquant sur 'Résoudre' avec le solveur gophersat.

## **6. Auteurs**
- Bouaita Rayane
- Trier Gabriel 