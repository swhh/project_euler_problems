from itertools import chain, permutations, product
import math
from cProfile import Profile
from pstats import Stats
from functools import cache
FILE = "p096_sudoku.txt"


def read_sudoku_files(file):
    with open(file, "r") as f:
        puzzle = []
        for i, line in enumerate(f):
            if i % 10 == 0:
                continue
            else:
                puzzle.append([int(char) for char in line[:-1]])
            if len(puzzle) == 9:
                yield puzzle
                puzzle = []


class Sudoku(object):
    def __init__(self, sudoku):
        self.puzzle = sudoku
        self.row_filled_positions = []
        self.row_numbers = []
        for row in self.puzzle:
            dic = {i: row[i] for i in range(9) if row[i]}
            self.row_filled_positions.append(dic)
            self.row_numbers.append(set(row))

    def get_row(self, puzzle_row):
        """Return number for position in puzzle"""
        return self.puzzle[puzzle_row]

    @cache
    def value_in_col(self, col, value, i):
        """Return true if value in puzzle col except row i"""
        for j in range(9):
            if j != i:
                if self.puzzle[j][col] == value:
                    return True
        return False

    def get_square(self, square_num):
        start_col = square_num % 3
        start_row = square_num - start_col
        rows = self.puzzle[start_row:start_row + 3]
        square = (row[start_col * 3:start_col * 3 + 3] for row in rows)
        return square, start_row

    @cache
    def value_in_square(self, square_num, value, i):
        """Return true if value in 3x3 square in square except row i"""
        square, start_row = self.get_square(square_num)
        for j, row in enumerate(square):
            if start_row + j != i:
                if value in row:
                    return True
        return False

    def __str__(self):
        grid = ''
        for i, row in enumerate(self.puzzle):
            grid += '|'.join(str(row[j * 3: j * 3 + 3]) for j in range(3))
            grid += '\n'
            if i % 3 == 2:
                grid += '\n'
        return grid


@cache
def find_square_num(row, col):
    return math.floor(row / 3) * 3 + math.floor(col / 3)


def filter_possibles(puzzle, possible_rows, row_num):
    for possible_row in possible_rows:
        impossible = False
        for i, entry in enumerate(possible_row):
            if puzzle.value_in_col(i, entry, row_num):
                impossible = True
                break
            square_num = find_square_num(row_num, i)
            if puzzle.value_in_square(square_num, entry, row_num):
                impossible = True
                break
        if impossible:
            continue
        else:
            yield possible_row


def possibles_fit(possible_one, possible_two, possible_three):
    for i in range(3):
        one = set(possible_one[i * 3: i + 3])
        two = set(possible_two[i * 3: i + 3])
        three = set(possible_three[i * 3: i + 3])
        if one.intersection(two) or two.intersection(three) or three.intersection(one):
            return False
    return True


def squares_possible_fit(square_one, square_two, square_three):
    rows_one = (set(triple) for triple in zip(*square_one))
    rows_two = (set(triple) for triple in zip(*square_two))
    rows_three = (set(triple) for triple in zip(*square_three))

    for a, b, c in zip(rows_one, rows_two, rows_three):
        if a.intersection(b) or b.intersection(c) or c.intersection(a):
            return False
    return True


def permute_update(permut, filled_positions):
    permut = list(permut)
    for key, val in filled_positions.items():
        permut.insert(key, val)
    return tuple(permut)


class FilterRows(object):
    def __init__(self, i, puzzle):
        self.i = i
        self.puzzle = puzzle

    def __iter__(self):
        filled_positions = self.puzzle.row_filled_positions[self.i]
        nums = self.puzzle.row_numbers[self.i]
        if not nums:
            possible_rows = permutations(range(1, 10))
        else:
            possibles = permutations(set(range(1, 10)) - nums)
            possible_rows = (permute_update(permut, filled_positions) for permut in possibles)
        possible_rows = filter_possibles(self.puzzle, possible_rows, self.i)
        yield from possible_rows


class FilterSquares(object):
    def __init__(self, i, possible_rows):
        self.i = i
        self.possible_rows = possible_rows

    def __iter__(self):
        possible_squares = (triple for triple in product(*self.possible_rows[self.i * 3: self.i * 3 + 3])
                            if possibles_fit(*triple))
        yield from possible_squares


def sudoku_solver(puzzle):
    """Find Sudoku solution for puzzle, return -1 if no solution"""
    all_possible_rows = []
    all_possible_squares = []

    for i in range(9):
        possible_rows = FilterRows(i, puzzle)
        all_possible_rows.append(possible_rows)

    for i in range(3):
        possible_squares = FilterSquares(i, all_possible_rows)
        all_possible_squares.append(possible_squares)

    for squares in product(*all_possible_squares):
        if squares_possible_fit(*squares):
            solution = chain.from_iterable(squares)
            return Sudoku(solution)
    return -1


def solve_sudokus(file):
    sudoku_puzzles = read_sudoku_files(file)
    for i, puzzle in enumerate(sudoku_puzzles):
        puzzle = Sudoku(puzzle)
        print(f'Sudoku Puzzle {i}\n')
        print(sudoku_solver(puzzle))


sudoku_files = read_sudoku_files(FILE)
first = next(sudoku_files)
second = next(sudoku_files)
third = next(sudoku_files)
fourth = next(sudoku_files)
fifth = next(sudoku_files)
sixth = next(sudoku_files)
seventh = next(sudoku_files)
puzzle = Sudoku(seventh)


test = lambda: sudoku_solver(puzzle)
profiler = Profile()
profiler.runcall(test)

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()

# if __name__ == '__main__':
#     solve_sudokus(FILE)



















