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
        """ get score from JSON file """
        if os.path.exists(self.scores_file):
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        else:
            return []  # Si le fichier n'existe pas, retourner une liste vide

    def save_scores(self):
        """ Save score in JSON file """
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f, indent=4)

    def add_score(self, name, score, time):
        """ Add score to save list """
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
            ("Personnaliser Terrain", self.show_customization_menu),
            ("Scores", self.show_scores),
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
                width=10,
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

    def show_customization_menu(self):
            """ print menu to custom grill """
            self.clear_window()

            customize_frame = tk.Frame(self.root, padx=20, pady=20)
            customize_frame.pack(expand=True)

            tk.Label(customize_frame, text="Personnalisez votre terrain", font=('Arial', 18)).pack(pady=20)

            # Select values
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
            """ Launch game with selected values """
            try:
                width = int(self.width_entry.get())
                height = int(self.height_entry.get())
                mines = int(self.mines_entry.get())

                # check values
                if width <= 0 or height <= 0 or mines <= 0 or mines >= width * height:
                    raise ValueError(
                        "Les valeurs doivent être positives et le nombre de mines doit être inférieur au nombre total de cellules.")

                self.clear_window()
                game = Game(width, height, mines)
                GameUI(self.root, game, self)
            except ValueError as e:
                messagebox.showerror("Erreur", f"Entrées invalides: {e}")

