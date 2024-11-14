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
        self.start_time = None  # add start timer
        self.initialize_grids()

    def initialize_grids(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.display_grid = [['?' for _ in range(self.width)] for _ in range(self.height)]

    def start_timer(self):
        """ start chrono """
        self.start_time = time.time()  # save depart time

    def get_elapsed_time(self):
        """ get time """
        if self.start_time is None:
            return 0  # if time dont start
        return round(time.time() - self.start_time)  # return time

    def place_mines(self, first_x: int, first_y: int):
        # start timer from first clic
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
        # check if value are in the window
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True  # ignore click outside of the window

        # put mine
        if self.first_move:
            self.place_mines(x, y)
            self.first_move = False

        # Ignore if flag
        if (x, y) in self.marked_cells:
            return True

        # end game if mine reveal
        if self.grid[y][x] == 'X':
            self.game_over = True
            return False

        # reveal clear cellul
        self.flood_fill(x, y)
        return True

    def flood_fill(self, x: int, y: int):
        # kepp clear cell
        visited = set()

        # explore adjacent cell with recursiv fonction
        def inner_fill(x, y):
            # check if cel not visit and in window
            if (x, y) in visited or not (0 <= x < self.width and 0 <= y < self.height):
                return

            # put cel mark
            visited.add((x, y))

            # reveal cel in grill
            self.display_grid[y][x] = str(self.grid[y][x])

            # if cell clear , explore adjacent cell
            if self.grid[y][x] == 0:
                for ax, ay in self.get_adjacent_cells(x, y):
                    inner_fill(ax, ay)

        # start adjacent clear
        inner_fill(x, y)

    def toggle_mark(self, x: int, y: int):
        if self.display_grid[y][x] == '?':
            # if normal cel, flag
            self.marked_cells.add((x, y))
            self.display_grid[y][x] = 'F'  # mark with flag
            print(f"Drapeau placé à la position ({x}, {y})")  # Debug
        elif self.display_grid[y][x] == 'F':
            # if mark cell, unmark
            self.marked_cells.remove((x, y))
            self.display_grid[y][x] = '?'  # normal print
            print(f"Retrait du drapeau à la position ({x}, {y})")  # Debug

    def check_win(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != 'X' and self.display_grid[y][x] == '?':
                    return False
        return len(self.marked_cells) == self.mines
