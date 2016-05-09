from SudokuStarter import SudokuBoard, init_board, is_complete
from copy import deepcopy
import time

class Cell(object):
    def __init__(self, row, col, board):
        self.row = row
        self.col = col
        self.board = board
        self.allowed_moves = []
        self.degree = 0

    def evalAllowedMoves(self):
        self.allowed_moves = self.board.get_allowed_moves(self.row, self.col)

    def evalDegree(self):
        # Check empty cells in row
        for col2 in range(0, self.board.BoardSize):
            if self.board.CurrentGameBoard[self.row][col2] == 0:
                self.degree += 1

        # Check empty cells in col
        for row2 in range(0, self.board.BoardSize):
            if self.board.CurrentGameBoard[row2][self.col] == 0:
                self.degree += 1

        # Check empty cells in cell, but not in row or col
        for row2, col2 in self.board.get_box_cells(self.row, self.col):
            if row2 == self.row or col2 == self.col:
                continue

            if self.board.CurrentGameBoard[row2][col2] == 0:
                self.degree += 1

class Node(object):
    counter = 0

    def __init__(self, board):
        self.board = board

    def epoch(self):
        # Return true if node is solved
        if is_complete(self.board):
            print "\n====== SOLVED ======"
            self.board.print_board()
            return True

        cells = []
        if SudokuBoard.mrv or SudokuBoard.degree:
            cells2 = []
            for [row, col] in self.board.empty_cells():
                cell = Cell(row, col, self.board)

                if SudokuBoard.mrv:
                    cell.evalAllowedMoves()
                if SudokuBoard.degree:
                    cell.evalDegree()

                cells2.append(cell)
            cells2 = sorted(cells2, key=lambda cell: (len(cell.allowed_moves), cell.degree))
            for cell in cells2:
                cells.append([cell.row, cell.col])
        else:
            # Get first empty cell
            cells = [self.board.first_empty_cell()]

        for [row, col] in [cells[0]]:
            if row == -1:
                print "NO EMPTY CELLS"
                self.board.print_board()
                return False

            # Try all values in empty cell
            #print "=== TESTING #" + str(Node.counter) + " ==="
            moves = range(1, self.board.BoardSize+1)

            if SudokuBoard.forcheck:
                moves = self.board.get_forcheck(row, col)

            if SudokuBoard.lcv:
                # Sort moves by lcv
                moves = sorted(moves, key=lambda move: self.board.get_lcv(row, col, move), reverse=True)


            for i in moves:
                # if Node.counter%5000 == 0:
                #     print Node.counter
                Node.counter+=1
                new_board = deepcopy(self.board)
                is_valid = new_board.set_value(row, col, i)
                if is_valid == False:
                    continue
                new_node = Node(new_board)
                if new_node.epoch():
                    return True

"""
SIZE = '25'
times = []
steps = []
for i in range(1,21):
    start = time.time()
    Node.counter = 0
    print "\n\n========== " + str(i) + " =========="
    sb = init_board("input_puzzles/more/" + SIZE + "x" + SIZE + "/" + SIZE + "x" + SIZE + "." + str(i) + ".sudoku")
    node = Node(sb)
    node.epoch()
    print Node.counter
    steps.append(Node.counter)
    times.append(time.time() - start)

for i in range(0, 20):
    print "\n===== " + str(i) + " ====="
    print "Time:  " + str(times[i])
    print "Steps: " + str(steps[i])

total_time = reduce(lambda x, y: x + y, times)
avg_time = total_time / len(times)
print "Total Time:   " + str(total_time)
print "Average Time: " + str(avg_time)

total_steps = reduce(lambda x, y: x + y, steps)
avg_step = total_steps / len(steps)
print "Total Steps:  " + str(total_steps)
print "Average Step: " + str(avg_step)
"""

sb = init_board("input_puzzles/easy/25_25.sudoku")
node = Node(sb)
node.epoch()
print Node.counter
