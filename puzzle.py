from queue import PriorityQueue
import curses
import time

INITIAL_STATE = [1, 4, 5, 7, 2, 3, 8, 6, 0]  # Set the initial state of environment. 0 denotes a blank tile.


class Board(object):
    """
        Board for the 8-Puzzle.
    """
    def __init__(self, board=None, moves=0, previous=None):
        self.board = board
        self.previous = previous
        self.moves = moves

    def is_goal(self):
        for i in range(0, 9):
            if i != 8:
                if self.board[i] != i + 1:
                    return False
        return True

    def move_blank(self, where):
        blank = self.find_blank()

        if where == 'left':
            if blank % 3 != 0:
                t_col = (blank % 3) - 1
                t_row = int(blank / 3)
                self.exchange(blank, t_row * 3 + t_col)

        elif where == 'right':
            if blank % 3 != 2:
                t_col = (blank % 3) + 1
                t_row = int(blank / 3)
                self.exchange(blank, t_row * 3 + t_col)

        elif where == 'up':
            if int(blank / 3) != 0:
                t_col = (blank % 3)
                t_row = int(blank / 3) - 1
                self.exchange(blank, t_row * 3 + t_col)

        elif where == 'down':
            if int(blank / 3) != 2:
                t_col = (blank % 3)
                t_row = int(blank / 3) + 1
                self.exchange(blank, t_row * 3 + t_col)

    def find_blank(self):
        blank = None
        for i in range(0, 9):
            if self.board[i] == 0:
                blank = i
                break
        return blank

    def clone(self):
        return Board(self.board.copy(), self.moves + 1, self)

    def exchange(self, source, target):
        self.board[source], self.board[target] = self.board[target], self.board[source]

    def neighbours(self):
        blank_index = self.find_blank()
        neighbours = []

        if blank_index % 3 != 0:
            new_board = self.clone()
            new_board.move_blank('left')
            neighbours.append(new_board)

        if blank_index % 3 != 2:
            new_board = self.clone()
            new_board.move_blank('right')
            neighbours.append(new_board)

        if int(blank_index / 3) != 0:
            new_board = self.clone()
            new_board.move_blank('up')
            neighbours.append(new_board)

        if int(blank_index / 3) != 2:
            new_board = self.clone()
            new_board.move_blank('down')
            neighbours.append(new_board)

        return neighbours

    def manhattan(self):
        manhattan = 0
        for i in range(0, 9):
            if self.board[i] != i + 1 and self.board[i] != 0:
                correct_pos = 8 if self.board[i] == 0 else self.board[i] - 1
                s_row = int(i / 3)
                s_col = i % 3
                t_row = int(correct_pos / 3)
                t_col = correct_pos % 3
                manhattan += abs(s_row - t_row) + abs(s_col - t_col)
        return manhattan

    def to_pq_entry(self, count):
        return self.moves + self.manhattan(), count, self

    def __str__(self):
        string = ''
        string = string + '+---+---+---+\n'
        for i in range(3):
            for j in range(3):
                tile = self.board[i * 3 + j]
                string = string + '| {} '.format(' ' if tile == 0 else tile)
            string = string + '|\n'
            string = string + '+---+---+---+\n'
        return string

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.board == other.board

    def get_previous_states(self):
        states = [self]
        prev = self.previous
        while prev is not None:
            states.append(prev)
            prev = prev.previous

        states.reverse()
        return states


def solve(initial_board):
    queue = PriorityQueue()
    queue.put(initial_board.to_pq_entry(0))

    i = 1
    while not queue.empty():
        board = queue.get()[2]
        if not board.is_goal():
            for neighbour in board.neighbours():
                if neighbour != board.previous:
                    queue.put(neighbour.to_pq_entry(i))
                    i += 1
        else:
            return board.get_previous_states()
    return None


def puzzle(window):
    initial = Board(board=INITIAL_STATE)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    window.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
    window.insstr(0, 0, 'Press any button to start!')
    window.insstr(1, 0, str(initial))
    window.getch()

    moves = solve(initial)
    window.clear()
    for move in moves:
        window.clear()
        window.insstr(0, 0, 'Solving puzzle: ')
        window.insstr(1, 0, str(move))
        window.refresh()
        time.sleep(1)

    window.insstr(8, 0, 'Puzzle solved.')
    window.getch()


if __name__ == '__main__':
    curses.wrapper(puzzle)
