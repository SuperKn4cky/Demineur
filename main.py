import tkinter as tk
from game import Game
from ui import GameUI
from menu import Menu

def main():
    root = tk.Tk()
    root.title("Démineur")
    menu = Menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()