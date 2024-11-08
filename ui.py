import tkinter as tk
from tkinter import messagebox
from game import Game
import tkinter.simpledialog as simpledialog


class GameUI:
    def __init__(self, root, game: Game, menu):
        self.root = root
        self.game = game
        self.menu = menu
        self.buttons = []
        self.create_game_ui()

    def create_game_ui(self):
        game_frame = tk.Frame(self.root)
        game_frame.pack(expand=True)

        # Grille de boutons
        for y in range(self.game.height):
            row = []
            for x in range(self.game.width):
                btn = tk.Button(game_frame, width=1, height=1)
                btn.grid(row=y, column=x)
                btn.bind('<Button-1>', lambda e, x=x, y=y: self.left_click(x, y))
                btn.bind('<Button-3>', lambda e, x=x, y=y: self.right_click(x, y))
                row.append(btn)
            self.buttons.append(row)

        # Bouton retour
        tk.Button(self.root, text="Retour au menu", command=self.menu.create_main_menu).pack(pady=10)

    def left_click(self, x: int, y: int):
        if not self.game.reveal_cell(x, y):
            self.show_all_mines()
            messagebox.showinfo("Game Over", "Vous avez perdu!")
            self.menu.create_main_menu()
        else:
            self.update_display()
            if self.game.check_win():
                messagebox.showinfo("Victoire", "Félicitations, vous avez gagné!")
                self.ask_player_name()

    def right_click(self, x: int, y: int):
        """ Gérer le clic droit :
            - Ajouter un drapeau
            - Retirer le drapeau
            - Revenir à l'état normal
        """
        if (x, y) in self.game.marked_cells:
            # Si la cellule est marquée avec un drapeau, on retire le drapeau
            self.game.toggle_mark(x, y)  # Retirer le drapeau
        else:
            # Si la cellule n'est pas marquée, on ajoute un drapeau
            self.game.toggle_mark(x, y)  # Ajouter le drapeau
        self.update_display()

    def update_display(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                value = self.game.display_grid[y][x]
                btn = self.buttons[y][x]

                if value == '?':
                    # Si la case est normale, on affiche rien
                    btn.config(text='', relief=tk.RAISED, bg="lightgray")
                elif value == 'F':
                    # Si la case est marquée avec un drapeau
                    btn.config(text='!', relief=tk.RAISED, bg="lightcoral")  # Drapeau (F)
                else:
                    # Affichage des valeurs numériques ou des mines
                    btn.config(text=value, relief=tk.SUNKEN, bg="lightgray")
                    if value == '0':
                        btn.config(text='')  # Enlever le texte si c'est un zéro

    def show_all_mines(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.grid[y][x] == 'X':
                    self.buttons[y][x].config(text='!', relief=tk.SUNKEN)

    def ask_player_name(self):
        name = tk.simpledialog.askstring("Victoire", "Entrez votre nom:")
        if name:
            time_taken = self.game.get_elapsed_time()  # Récupérer le temps écoulé
            self.menu.add_score(name, self.game.mines, time_taken)  # Ajouter le score avec le temps

