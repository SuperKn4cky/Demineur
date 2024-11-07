import tkinter as tk
from tkinter import messagebox
from game import Game
from ui import GameUI
import json
import os


class Menu:
    def __init__(self, root):
        self.root = root
        self.scores_file = 'high_scores.json'  # Fichier JSON pour les scores
        self.scores = self.load_scores()  # Charger les scores depuis le fichier JSON
        self.create_main_menu()

    def load_scores(self):
        """ Charge les scores depuis le fichier JSON """
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        else:
            return []  # Si le fichier n'existe pas, retourner une liste vide

    def save_scores(self):
        """ Sauvegarde les scores dans le fichier JSON """
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f, indent=4)

    def add_score(self, name, score, time):
        """ Ajouter un score à la liste et sauvegarder """
        self.scores.append({"name": name, "score": score, "time": time})  # Ajout du temps
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)  # Trier les scores
        self.save_scores()

    def create_main_menu(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True)

        tk.Label(main_frame, text="DÉMINEUR", font=('Arial', 24, 'bold')).pack(pady=20)

        buttons = [
            ("Nouvelle Partie", self.show_difficulty_menu),
            ("Scores", self.show_scores),
            ("Rejouer une Grille", self.show_saved_grids),
            ("Quitter", self.root.quit)
        ]

        for text, command in buttons:
            tk.Button(main_frame, text=text, command=command, width=20).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_difficulty_menu(self):
        self.clear_window()

        diff_frame = tk.Frame(self.root, padx=20, pady=20)
        diff_frame.pack(expand=True)

        tk.Label(diff_frame, text="Choisissez la difficulté", font=('Arial', 18)).pack(pady=20)

        difficulties = {
            "Facile": (3, 3, 3),
            "Moyen": (16, 16, 40),
            "Difficile": (30, 16, 99)
        }

        for name, (width, height, mines) in difficulties.items():
            tk.Button(
                diff_frame,
                text=name,
                command=lambda w=width, h=height, m=mines: self.start_game(w, h, m)
            ).pack(pady=5)

        tk.Button(diff_frame, text="Retour", command=self.create_main_menu).pack(pady=20)

    def start_game(self, width, height, mines):
        self.clear_window()
        game = Game(width, height, mines)
        GameUI(self.root, game, self)

    def show_scores(self):
        self.clear_window()
        scores_frame = tk.Frame(self.root, padx=20, pady=20)
        scores_frame.pack(expand=True)

        tk.Label(scores_frame, text="Meilleurs Scores", font=('Arial', 18)).pack(pady=20)

        if not self.scores:
            tk.Label(scores_frame, text="Aucun score enregistré").pack()
        else:
            for score in self.scores:
                time_taken = score.get('time', 'Inconnu')  # Utilisation de 'Inconnu' si la clé 'time' est absente
                tk.Label(
                    scores_frame,
                    text=f"{score['name']} - {score['score']} mines - {time_taken} secondes"
                ).pack()

        tk.Button(scores_frame, text="Retour", command=self.create_main_menu).pack(pady=20)

    def show_saved_grids(self):
        self.clear_window()
        grids_frame = tk.Frame(self.root, padx=20, pady=20)
        grids_frame.pack(expand=True)

        tk.Label(grids_frame, text="Grilles Sauvegardées", font=('Arial', 18)).pack(pady=20)

        saved_grids = self.db.get_saved_grids()  # Cette partie dépend de ta logique de sauvegarde de grille
        if not saved_grids:
            tk.Label(grids_frame, text="Aucune grille sauvegardée").pack()
        else:
            for grid in saved_grids:
                tk.Button(
                    grids_frame,
                    text=f"Grille de {grid['name']} - {grid['difficulty']}",
                    command=lambda g=grid: self.load_saved_grid(g)
                ).pack(pady=5)

        tk.Button(grids_frame, text="Retour", command=self.create_main_menu).pack(pady=20)

    def load_saved_grid(self, grid_data):
        self.clear_window()
        grid_info = grid_data['grid_data']
        game = Game(grid_info['width'], grid_info['height'], grid_info['mines'])
        game.grid = grid_info['grid']
        game.calculate_numbers()
        GameUI(self.root, game, self)
