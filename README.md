# **Flow_Free_Solver**

## **1. Mémo**

### **Objectif du Projet**

Le but de ce projet est de **résoudre le puzzle « Flow Free / Connecting Dots » par réduction en SAT**. Concrètement, il s’agit de :

- **Trouver une affectation de couleurs** aux éléments (arêtes) d’un graphe dérivé d’une grille afin de relier, par des chemins continus, des paires de points terminaux de même couleur.
- **Remplir entièrement la grille** avec des chemins (un pour chaque couleur) qui ne se croisent pas et respectent les règles du jeu.

### **Règles du Jeu**

Dans le jeu **Flow Free**, la grille contient plusieurs paires de points colorés. Chaque paire doit être reliée par un chemin continu, et les règles imposent que :

- **Chaque cellule intermédiaire** (non terminale) doit être traversée par exactement **deux arêtes** de la même couleur (représentant l’entrée et la sortie du chemin).
- **Chaque cellule terminale** (le point coloré) doit être connectée à exactement **une arête** de la même couleur.

## **2. Modélisation et Contraintes**

Pour résoudre le puzzle, nous réduisons le problème à une instance SAT en modélisant la grille sous forme d’un **graphe**. Voici les éléments clés :

### **Définitions des Variables**

- **e** : une **arête** du graphe.  
  Une arête représente une connexion entre deux cellules adjacentes de la grille (voisinage haut, bas, gauche, droite).

- **c** : une **couleur** parmi celles autorisées dans le puzzle.  

- **x(e, c)** : une variable booléenne associée à l'arête **e** et à la couleur **c**.  
  
  Par exemple: **x(e, c) = True** signifie que l'arête **e** est utilisée dans la solution et affectée de la couleur **c**.

### **Les Contraintes**

1. **Contrainte sur les Arêtes :**  
   **Chaque arête doit avoir exactement une couleur.**  
   Pour chaque arête **e**, et pour toute paire de couleurs distinctes (c1) et (c2), la clause suivante est ajoutée :
   - **Clause :**  
     $$
     \lnot \bigl(x(e, c_1) \land x(e, c_2)\bigr)
     $$
     ou équivalent en CNF :
     $$
     \bigl(\lnot x(e, c_1) \lor \lnot x(e, c_2)\bigr)
     $$

2. **Contraintes sur les Nœuds Connecteurs (Non Terminaux) :**  
   **Chaque nœud non terminal doit être traversé par exactement deux arêtes incidentes, et ces deux arêtes doivent être de la même couleur.**  
   - **(a) Cardinalité :**  
     Pour un nœud \( v \) non terminal, considérant l’ensemble \( E(v) \) des arêtes incidentes à \( v \), on impose que la somme des variables \( x(e, c) \) (pour toutes les couleurs **c** et pour tous \( e in E(v) \)) est exactement égale à 2.
   - **(b) Uniformité de Couleur :**  
     Pour chaque paire d’arêtes (e1, e2) incidentes à \( v \) et pour toute paire de couleurs distinctes (c1) et (c2), on ajoute la clause :
     - **Clause :**  
       $$
       \lnot x(e_1, c_1) \lor \lnot x(e_2, c_2) \quad \text{si } c_1 \neq c_2.
       $$
     Cela interdit que deux arêtes incidentes utilisées aient des couleurs différentes.

3. **Contraintes sur les Nœuds Terminaux :**  
   Chaque nœud terminal doit être connecté par exactement une arête, et cette arête doit être de la couleur imposée par le terminal.
   

## **3. Démarche Suivie**

1. **Modélisation du Problème sous Forme de Graphe**  
   La grille est transformée en graphe où chaque cellule est un nœud et les arêtes représentent les connexions possibles entre cellules adjacentes.

2. **Réduction en Instance SAT**  
   Les contraintes du jeu (décrites ci-dessus) sont traduites en clauses CNF. Les variables \( x(e, c) \) représentent la décision d’affecter la couleur **c** à l’arête **e**.

3. **Utilisation d’un Solveur SAT**  
   Un solveur SAT (tel que **Glucose3** via la bibliothèque `python-sat`) est utilisé pour trouver une affectation satisfaisante qui respecte l’ensemble des contraintes.

4. **Affichage de la Solution**  
   La solution SAT est interprétée pour afficher, via une interface graphique (Tkinter), la grille et les chemins (arêtes colorées) reliant les terminaux.

---

## **4. Architecture du Projet**

Le projet est organisé de manière modulaire avec plusieurs fichiers :

- **`puzzle.py`**  
  Définit la classe **`Puzzle`** qui représente un puzzle en termes de dimension de la grille et d’assignation des nœuds terminaux (leur position et leur couleur).

- **`sat_solver.py`**  
  Construit l’instance SAT en traduisant les contraintes du puzzle en clauses CNF et en associant une variable \( x(e, c) \) pour chaque arête **e** et chaque couleur **c**.

- **`gui.py`**  
  Contient le module d’affichage graphique utilisant **Tkinter** pour visualiser la solution trouvée par le solveur SAT.

- **`main.py`**  
  Le fichier principal qui :
  - Charge la configuration du puzzle depuis un fichier de configuration.
  - Crée le puzzle et construit l’instance SAT.
  - Résout le problème avec le solveur SAT.
  - Affiche la solution via l’interface graphique.

- **`puzzles/`**  
  Ce dossier contient plusieurs fichiers de configuration (par exemple, `puzzle1.py`, `puzzle2.py`, etc.) qui définissent des puzzles sous la forme de dictionnaires.

---

## **5. Installation et Exécution**

### **Prérequis**

- **Python 3.x**
- **Bibliothèque `python-sat`** pour le solveur SAT  
- **Tkinter** pour l'affichage graphique (généralement inclus avec Python)

### **Installation des Dépendances**

Exécutez la commande suivante pour installer la bibliothèque SAT :

```bash
pip install python-sat
```
## **6. Auteurs**
- Bouaita Rayane
- Trier Gabriel 