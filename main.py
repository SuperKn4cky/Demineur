import tkinter as tk
from menu import Menu

def main():
    root = tk.Tk()
    root.title("Démineur")
    Menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()