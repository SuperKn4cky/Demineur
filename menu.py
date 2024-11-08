import tkinter as tk
from tkinter import messagebox
from game import Game
from ui import GameUI


class Menu:
    def __init__(self, root):
        self.root = root
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True)

        tk.Label(main_frame, text="DÉMINEUR", font=('Arial', 24, 'bold')).pack(pady=20)

        buttons = [
            ("Nouvelle Partie", self.show_difficulty_menu),
            ("Personnaliser Terrain", self.show_customization_menu),  # Bouton pour personnalisation
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
            "Facile": (9, 9, 10),
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

    def show_customization_menu(self):
        """ Affiche un menu pour personnaliser la grille """
        self.clear_window()

        customize_frame = tk.Frame(self.root, padx=20, pady=20)
        customize_frame.pack(expand=True)

        tk.Label(customize_frame, text="Personnalisez votre terrain", font=('Arial', 18)).pack(pady=20)

        # Saisie de la largeur, hauteur et nombre de mines
        tk.Label(customize_frame, text="Largeur :").pack(pady=5)
        self.width_entry = tk.Entry(customize_frame)
        self.width_entry.pack(pady=5)
        self.width_entry.insert(tk.END, "10")  # Valeur par défaut

        tk.Label(customize_frame, text="Hauteur :").pack(pady=5)
        self.height_entry = tk.Entry(customize_frame)
        self.height_entry.pack(pady=5)
        self.height_entry.insert(tk.END, "10")  # Valeur par défaut

        tk.Label(customize_frame, text="Nombre de mines :").pack(pady=5)
        self.mines_entry = tk.Entry(customize_frame)
        self.mines_entry.pack(pady=5)
        self.mines_entry.insert(tk.END, "10")  # Valeur par défaut

        tk.Button(customize_frame, text="Lancer la Partie", command=self.start_custom_game).pack(pady=10)
        tk.Button(customize_frame, text="Retour", command=self.create_main_menu).pack(pady=10)

    def start_custom_game(self):
        """ Lance la partie personnalisée avec les valeurs saisies """
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            mines = int(self.mines_entry.get())

            # Vérification des valeurs
            if width <= 0 or height <= 0 or mines <= 0 or mines >= width * height:
                raise ValueError(
                    "Les valeurs doivent être positives et le nombre de mines doit être inférieur au nombre total de cellules.")

            self.clear_window()
            game = Game(width, height, mines)
            GameUI(self.root, game, self)
        except ValueError as e:
            messagebox.showerror("Erreur", f"Entrées invalides: {e}")

    def start_game(self, width, height, mines):
        self.clear_window()
        game = Game(width, height, mines)
        GameUI(self.root, game, self)

    def show_scores(self):
        self.clear_window()
        scores_frame = tk.Frame(self.root, padx=20, pady=20)
        scores_frame.pack(expand=True)

        tk.Label(scores_frame, text="Meilleurs Scores", font=('Arial', 18)).pack(pady=20)

        scores = self.db.get_high_scores()
        if not scores:
            tk.Label(scores_frame, text="Aucun score enregistré").pack()
        else:
            for score in scores:
                tk.Label(
                    scores_frame,
                    text=f"{score['name']} - {score['score']} mines - {score['time']} secondes"
                ).pack()

        tk.Button(scores_frame, text="Retour", command=self.create_main_menu).pack(pady=20)

    def show_saved_grids(self):
        self.clear_window()
        grids_frame = tk.Frame(self.root, padx=20, pady=20)
        grids_frame.pack(expand=True)

        tk.Label(grids_frame, text="Grilles Sauvegardées", font=('Arial', 18)).pack(pady=20)

        saved_grids = self.db.get_saved_grids()
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
