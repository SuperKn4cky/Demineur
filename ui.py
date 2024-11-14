import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from game import Game


class GameUI:
    def __init__(self, root, game: Game, menu):
        self.root = root
        self.game = game
        self.menu = menu
        self.buttons = []
        self.create_game_ui()

    def create_game_ui(self):
        game_frame = tk.Frame(self.root)
        game_frame.pack(expand=True, fill="both")

        # Grille de boutons
        for y in range(self.game.height):
            row = []
            for x in range(self.game.width):
                btn = tk.Button(game_frame, width=1, height=1)  # Taille augmentée pour uniformité avec Label
                btn.grid(row=y, column=x, sticky="nsew")  # Utilisation de `sticky` pour occuper l'espace
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
            self.update_cell(x, y)
            self.update_display()
            if self.game.check_win():
                messagebox.showinfo("Victoire", "Félicitations, vous avez gagné!")
                self.ask_player_name()

    def right_click(self, x: int, y: int):
        if (x, y) in self.game.marked_cells:
            self.game.toggle_mark(x, y)
        else:
            self.game.toggle_mark(x, y)
        self.update_display()

    def update_display(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                self.update_cell(x, y)

    def update_cell(self, x, y):
        """Met à jour l'apparence de la cellule après sa révélation."""
        value = self.game.display_grid[y][x]

        # Couleurs associées à chaque nombre de mines adjacentes
        colors = {
            '1': 'blue',
            '2': 'green',
            '3': 'red',
            '4': 'darkblue',
            '5': 'darkred',
            '6': 'turquoise',
            '7': 'black',
            '8': 'gray'
        }

        if value != '?' and value != 'F':
            # Configurer le bouton pour ressembler à une cellule révélée
            self.buttons[y][x].config(
                text=value if value != '0' else '',
                relief=tk.SUNKEN,
                bg="white",
                fg=colors.get(value, "black"),
                activebackground="white",
                activeforeground=colors.get(value, "black"),
                state="normal",
                takefocus=0,
                highlightthickness=0,
                bd=0
            )
        elif value == 'F':
            self.buttons[y][x].config(
                text='!',
                relief=tk.RAISED,
                bg="lightcoral",
                activebackground="lightcoral",
                activeforeground="black",
                takefocus=0
            )
        else:
            self.buttons[y][x].config(
                text='',
                relief=tk.RAISED,
                bg="lightgray",
                activebackground="lightgray",
                activeforeground="black",
                takefocus=0
            )

    def show_all_mines(self):
        for y in range(self.game.height):
            for x in range(self.game.width):
                if self.game.grid[y][x] == 'X':
                    self.buttons[y][x].config(text='!', relief=tk.SUNKEN, bg="red")

    def ask_player_name(self):
        name = tk.simpledialog.askstring("Victoire", "Entrez votre nom:")
        if name:
            time_taken = self.game.get_elapsed_time()
            self.menu.add_score(name, self.game.mines, time_taken)
