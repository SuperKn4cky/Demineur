import random
from typing import List, Tuple, Set
import time


class Game:
    def __init__(self, width: int, height: int, mines: int):
        self.width = width
        self.height = height
        self.mines = mines
        self.grid = None
        self.display_grid = None
        self.first_move = True
        self.game_over = False
        self.marked_cells = set()
        self.start_time = None  # Ajout du temps de début
        self.initialize_grids()

    def initialize_grids(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.display_grid = [['?' for _ in range(self.width)] for _ in range(self.height)]

    def start_timer(self):
        """ Démarre le chronomètre pour le jeu """
        self.start_time = time.time()  # Enregistrer l'heure de départ

    def get_elapsed_time(self):
        """ Récupère le temps écoulé en secondes """
        if self.start_time is None:
            return 0  # Si le chronomètre n'a pas encore démarré
        return round(time.time() - self.start_time)  # Retourne le temps écoulé en secondes

    def place_mines(self, first_x: int, first_y: int):
        # Démarre le chronomètre dès le premier clic
        if self.first_move:
            self.start_timer()

        safe_cells = {(first_x, first_y)}
        safe_cells.update(self.get_adjacent_cells(first_x, first_y))

        available_cells = [(x, y) for x in range(self.width) for y in range(self.height)
                           if (x, y) not in safe_cells]

        mine_positions = random.sample(available_cells, self.mines)

        for x, y in mine_positions:
            self.grid[y][x] = 'X'

        self.calculate_numbers()

    def calculate_numbers(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != 'X':
                    count = sum(1 for ax, ay in self.get_adjacent_cells(x, y)
                                if 0 <= ax < self.width and 0 <= ay < self.height
                                and self.grid[ay][ax] == 'X')
                    self.grid[y][x] = count

    def get_adjacent_cells(self, x: int, y: int) -> List[Tuple[int, int]]:
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    adjacent.append((new_x, new_y))
        return adjacent

    def reveal_cell(self, x: int, y: int) -> bool:
        # Vérifie si les coordonnées sont dans les limites de la grille
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True  # Ignore les clics hors de la grille

        # Placement des mines lors du premier clic
        if self.first_move:
            self.place_mines(x, y)
            self.first_move = False

        # Ignore si la cellule est marquée comme drapeau
        if (x, y) in self.marked_cells:
            return True

        # Si une mine est révélée, fin de la partie
        if self.grid[y][x] == 'X':
            self.game_over = True
            return False

        # Révèle les cellules avec la propagation
        self.flood_fill(x, y)
        return True

    def flood_fill(self, x: int, y: int):
        # Ensemble pour garder une trace des cellules déjà visitées
        visited = set()

        # Fonction interne récursive pour explorer les cellules adjacentes
        def inner_fill(x, y):
            # Vérifie si la cellule est dans les limites de la grille et n'a pas encore été visitée
            if (x, y) in visited or not (0 <= x < self.width and 0 <= y < self.height):
                return

            # Marque la cellule comme visitée
            visited.add((x, y))

            # Révèle la cellule dans la grille d'affichage
            self.display_grid[y][x] = str(self.grid[y][x])

            # Si la cellule est vide (0), continue à explorer les cellules adjacentes
            if self.grid[y][x] == 0:
                for ax, ay in self.get_adjacent_cells(x, y):
                    inner_fill(ax, ay)

        # Lancement de la propagation à partir de la cellule initiale
        inner_fill(x, y)

    def toggle_mark(self, x: int, y: int):
        """ Alterne entre les trois états : normal, marqué avec un drapeau, et état normal. """
        if self.display_grid[y][x] == '?':
            # Si la cellule est normale, on marque avec un drapeau
            self.marked_cells.add((x, y))
            self.display_grid[y][x] = 'F'  # Marquer avec un drapeau
            print(f"Drapeau placé à la position ({x}, {y})")  # Debug
        elif self.display_grid[y][x] == 'F':
            # Si la cellule est marquée avec un drapeau, on la retire
            self.marked_cells.remove((x, y))
            self.display_grid[y][x] = '?'  # Revenir à l'état normal
            print(f"Retrait du drapeau à la position ({x}, {y})")  # Debug

    def check_win(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != 'X' and self.display_grid[y][x] == '?':
                    return False
        return len(self.marked_cells) == self.mines
