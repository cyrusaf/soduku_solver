from SudokuStarter import SudokuBoard, init_board, is_complete
from copy import deepcopy
import time

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

        # Get first empty cell
        [row, col] = self.board.first_empty_cell()

        if row == -1:
            print "NO EMPTY CELLS"
            self.board.print_board()
            return False

        # Try all values in empty cell
        #print "=== TESTING #" + str(Node.counter) + " ==="
        moves = range(1, self.board.BoardSize+1)

        if SudokuBoard.forcheck:
            moves = self.board.get_forcheck(row, col)

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

times = []
steps = []
for i in range(1,21):
    start = time.time()
    Node.counter = 0
    print "\n\n========== " + str(i) + " =========="
    sb = init_board("input_puzzles/more/9x9/9x9." + str(i) + ".sudoku")
    node = Node(sb)
    node.epoch()
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
