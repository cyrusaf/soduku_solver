#!/usr/bin/env python
import struct, string, math
from copy import deepcopy

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    forcheck = True
    mrv      = True
    degree   = True
    lcv      = True

    def __init__(self, size, board):
        """the constructor for the SudokuBoard"""
        self.BoardSize = size #the size of the board
        self.BoxSize   = int(math.sqrt(size))
        self.CurrentGameBoard= board #the current state of the game board
        self.init = False

        if SudokuBoard.forcheck:
            self.ForCheck = []
            for row in range(0, self.BoardSize):
                new_row = []
                for col in range(0, self.BoardSize):
                    new_row.append(self.get_allowed_moves(row, col))
                self.ForCheck.append(new_row)
            self.init = True

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        if self.is_valid_move(row, col, value):
            #add the value to the appropriate position on the board
            self.CurrentGameBoard[row][col]=value

            # Set forcheck values to false for row, col, and block
            if SudokuBoard.forcheck:
                # Row
                for col2 in range(0,self.BoardSize):
                    self.ForCheck[row][col2][value-1] = False

                # Col
                for row2 in range(0,self.BoardSize):
                    self.ForCheck[row2][col][value-1] = False

                # Block
                box_cells = self.get_box_cells(row, col)
                for [row2, col2] in box_cells:
                    self.ForCheck[row2][col2][value-1] = False

            return True

        return False

    def empty_cells(self):
        """Gets empty cells of board"""
        empty_cells = []
        for row in range(0, self.BoardSize):
            for col in range(0, self.BoardSize):
                if self.CurrentGameBoard[row][col] == 0:
                    empty_cells.append([row, col])
        return empty_cells

    def first_empty_cell(self):
        """Gets the first empty cell in the board"""
        for row in range(0, self.BoardSize):
            for col in range(0, self.BoardSize):
                if self.CurrentGameBoard[row][col] == 0:
                    return [row, col]

        return [-1, -1]

    def get_allowed_moves(self, row, col):
        """Get allowed moves for a cell"""
        if SudokuBoard.forcheck and self.init:
            moves = []
            for i, val in enumerate(self.ForCheck[row][col]):
                if val:
                    moves.append(i+1)
            return moves

        allowed_moves = []
        for i in range(0,self.BoardSize):
            allowed_moves.append(True)

        cell = self.CurrentGameBoard[row][col]
        if cell != 0:
            return [False]*self.BoardSize

        # Check row
        for col2 in range(0, self.BoardSize):
            cell2 = self.CurrentGameBoard[row][col2]
            if cell2 == 0:
                continue
            allowed_moves[cell2-1] = False

        # Check col
        for row2 in range(0, self.BoardSize):
            cell2 = self.CurrentGameBoard[row2][col]
            if cell2 == 0:
                continue
            allowed_moves[cell2-1] = False

        # Check box
        for [row2, col2] in self.get_box_cells(row, col):
            cell2 = self.CurrentGameBoard[row2][col2]
            if cell2 == 0:
                continue
            allowed_moves[cell2-1] = False

        moves = []
        for i in range(0, self.BoardSize):
            if allowed_moves[i]:
                moves.append(i+1)

        return allowed_moves

    def get_forcheck(self, row, col):
        allowed_moves = []
        for i, allowed in enumerate(self.ForCheck[row][col]):
            if allowed:
                allowed_moves.append(i+1)
        return allowed_moves


    def is_valid_move(self, row, col, value):
        """Check if move is valid"""
        cell = self.CurrentGameBoard[row][col]
        if cell != 0:
            return []

        # Check row
        for col2 in range(0, self.BoardSize):
            if col2 == col:
                continue
            cell2 = self.CurrentGameBoard[row][col2]
            if cell2 == value:
                return False

        # Check col
        for row2 in range(0, self.BoardSize):
            if row2 == row:
                continue
            cell2 = self.CurrentGameBoard[row2][col]
            if cell2 == value:
                return False

        # Check box
        for [row2, col2] in self.get_box_cells(row, col):
            if row2 == row and col2 == col:
                continue
            cell2 = self.CurrentGameBoard[row2][col2]
            if cell2 == value:
                return False

        return True

    def dead_end(self):
        """Check if board is a dead end"""
        for [row, col] in self.empty_cells():
            allowed_moves = self.get_allowed_moves(row, col)
            if len(allowed_moves) == 0:
                return True
        return False

    def get_box_pos(self, row, col):
        box_row = math.floor(row/self.BoxSize)
        box_col = math.floor(col/self.BoxSize)
        return [box_row, box_col]

    def get_box_cells(self, row, col):
        box_cells = []

        [box_row, box_col] = self.get_box_pos(row, col)

        for r in range(0, self.BoxSize):
            for c in range(0, self.BoxSize):
                box_cells.append([int(box_row*self.BoxSize+r), int(box_col*self.BoxSize+c)])

        return box_cells

    def get_frontier(self):
        frontier = []
        for [row, col] in self.empty_cells():
            allowed_moves = self.get_allowed_moves(row, col)
            for move in allowed_moves:
                new_board = deepcopy(self)
                new_board.set_value(row, col, move)
                # if new_board.dead_end():
                #     continue
                frontier.append(new_board)
        return frontier

    def get_lcv(self, row, col, val):
        lcv = 0
        # Check cells in row
        for col2 in range(0, self.BoardSize):
            allowed_moves = self.get_allowed_moves(row, col2)
            if val in allowed_moves:
                lcv += 1

        # Check cells in col
        for row2 in range(0, self.BoardSize):
            allowed_moves = self.get_allowed_moves(row2, col)
            if val in allowed_moves:
                lcv += 1

        # Check cells in cell, but not in row or col
        for row2, col2 in self.get_box_cells(row, col):
            if row2 == row or col2 == col:
                continue

            allowed_moves = self.get_allowed_moves(row2, col2)
            if val in allowed_moves:
                lcv += 1

        return lcv

    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val

    return board

def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    print "Your code will solve the initial_board here!"
    print "Remember to return the final board (the SudokuBoard object)."
    print "I'm simply returning initial_board for demonstration purposes."
    return initial_board
