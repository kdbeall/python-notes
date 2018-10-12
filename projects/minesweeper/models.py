""" Data models for a minesweeper CLI game. """

import random
import itertools
from enum import Enum

class GameState(Enum):
    start = 0
    win = 1
    lose = 2
    on_going = 3

class Board:
    """ Represents a minesweeper board with squares. """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.game_state = GameState.start
        self.number_of_mines = 0
        self.max_mines = (cols-1)*(rows-1)
        mines_percentage = (100 * self.max_mines / (rows*cols))/3
        self.__create_squares(self.cols, self.rows, mines_percentage)
    

    def flag_square(self, row, col):
        if not self.__valid_square(row, col):
            return False
        if self.__get_square(row, col).clicked:
            return False
        square = self.squares[row][col]
        square.flag = not square.flag

    def click_square(self, row, col):
        """ 
            Click the square and click its
            neighbors which don't have neighboring mines.
        """
        if not self.__valid_square(row, col) or self.__get_square(row, col).clicked:
            return
        square = self.squares[row][col]
        if self.game_state == GameState.start:
            square.mine = False
            for neighbor in square.neighbors():
                neighbor.mine = False
            self.game_state = GameState.on_going
        if square.mine:
            self.game_state = GameState.lose
            return
        square.clicked = True
        if square.mine_neighbors() == 0:
            for neighbor in square.neighbors():
                if not neighbor.mine:
                    if neighbor.mine_neighbors() == 0:
                        self.click_square(neighbor.row, neighbor.col)
                    neighbor.clicked = True
        if self.__win():
            self.game_state = GameState.win

    def print_board(self):
        """
            Prints the board. If a square is clicked, 
            print the number of neighboring mines.
            If the square is flagged, print "f".
            Else print ".".
        """
        print("\n")
        col_print = "    "
        for i in range(0, self.cols):
            col_print += str(i) + "  "
        print(col_print + "\n")
        for i,row in enumerate(self.squares):
            row_print = str(i) + "  "
            for i, square in enumerate(row):
                if square.clicked:
                    row_print += " " + str(square.mine_neighbors()) + " "
                elif square.flag:
                    row_print += " f "
                else:
                    row_print += " . "
            print(row_print + "\n\n")

    def print_board_end(self):
        col_print = "    "
        for i in range(0, self.cols):
            col_print += str(i) + "  "
        print(col_print + "\n")
        for i,row in enumerate(self.squares):
            row_print = str(i) + "  "
            for i, square in enumerate(row):
                if square.mine:
                    row_print += " x "
                elif square.clicked:
                    row_print += " " + str(square.mine_neighbors()) + " "
                elif square.flag:
                    row_print += " f "    
                else:
                    row_print += " . "
            print(row_print + "\n\n")
        

    def __win(self):
        for row in self.squares:
            for square in row:
                if not square.mine and not square.clicked:
                    return False
        return True

    def __get_square(self, row, col):
        """ Return the square at the given row and column."""
        return self.squares[row][col]

    def __valid_square(self, row, col):
        return (row < self.rows and row >= 0) and (col < self.cols and col >= 0)

    def __create_squares(self, cols, rows, mines_percentage):
        """
            Create a grid of squares of size rows by cols.
        """
        self.squares = [[Square(self, row, col, mine=self.__is_mine(mines_percentage))
                        for col in range(cols)] for row in range(rows)]

    def __is_mine(self, mines_percentage):
        """ Determine if a square is a mine while generating the board. """
        is_mine = random.randrange(100) < mines_percentage
        if is_mine:
            if self.number_of_mines >= self.max_mines:
                return False
            self.number_of_mines = self.number_of_mines + 1
            return True
        return False
       


class Square:
    """
        Represents a single square in the minesweeper board.
        A square may have or may not have a mine, may be clicked or unclicked.
    """
    def __init__(self, board, row, col, mine):
        self.board = board
        self.row = row
        self.col = col
        self.mine = mine
        self.flag = False
        self.clicked = False

    def mine_neighbors(self):
        return len(list(filter(lambda square: square.mine, [self.board.squares[point[0]][point[1]] for point in self.__point_neighbors()])))

    def neighbors(self):
        return [self.board.squares[point[0]][point[1]] for point in self.__point_neighbors()]

    def __point_neighbors(self):
        row_neighbors = list(filter(lambda val: val >= 0 and val < self.board.rows, [self.row-1, self.row, self.row+1])) 
        col_neighbors = list(filter(lambda val: val >= 0 and val < self.board.cols, [self.col-1, self.col, self.col+1]))
        neighbor_set = set(itertools.product(row_neighbors, col_neighbors))
        neighbor_set.remove((self.row, self.col))
        return list(neighbor_set)