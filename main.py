import timeit

import level
from render import SudokuImage


class Sudoku:
    def __init__(self, matrix):
        self.matrix = matrix

    def __repr__(self):
        return "\n".join(
            "  ".join(map(lambda x: str(x) if isinstance(x, int) else "-", line))
            for line in self.matrix)

    def details(self):
        return "\n".join(
            "\t".join(map(lambda x: str(x), line))
            for line in self.matrix)

    def solve(self):
        return self.difference(*self.get_fills()) or self.elimination(*self.get_possibles())

    def difference(self, squares, horizontals, verticals) -> int:
        count = 0

        full = set(range(1, 10))
        for y in range(9):
            for x in range(9):
                if isinstance(self.matrix[y][x], set):
                    new = full - squares[y // 3][x // 3] - horizontals[y] - verticals[x]
                    if len(new) > 1:
                        self.matrix[y][x] = new
                    else:
                        self.matrix[y][x] = new.pop()
                        count += 1
        return count

    def elimination(self, squares, horizontals, verticals):
        count = 0
        for y in range(9):
            for x in range(9):
                if isinstance(array := self.matrix[y][x], set):
                    for value in set(array):
                        if squares[y // 3][x // 3].count(value) == 1 or\
                                horizontals[y].count(value) == 1 or \
                                verticals[x].count(value) == 1:
                            self.matrix[y][x] = value
                            count += 1
                            break
        return count

    def selection(self, squares, horizontals, verticals):
        pass

    def get_fills(self):
        squares = [[set() for _ in range(3)] for _ in range(3)]
        horizontals = [set() for _ in range(9)]
        verticals = [set() for _ in range(9)]
        for y in range(9):
            for x in range(9):
                if isinstance(value := self.matrix[y][x], int):
                    squares[y // 3][x // 3].add(value)
                    horizontals[y].add(value)
                    verticals[x].add(value)
        return squares, horizontals, verticals

    def get_possibles(self):
        squares = [[[] for _ in range(3)] for _ in range(3)]
        horizontals = [[] for _ in range(9)]
        verticals = [[] for _ in range(9)]
        for y in range(9):
            for x in range(9):
                if isinstance(array := self.matrix[y][x], set):
                    squares[y // 3][x // 3] += (list(array))
                    horizontals[y] += (list(array))
                    verticals[x] += list(array)
        return squares, horizontals, verticals


def main():
    with open(level.HARD, "r") as f:
        matrix = [list(map(lambda x: int(x) if x.isdigit() else set(), line)) for line in map(str.strip, f.readlines())]

    sudoku = Sudoku(matrix)
    while sudoku.solve():
        pass

    start = timeit.default_timer()
    k = 14
    size = (k * 630, k * 630)
    SudokuImage(sudoku.matrix, size).display()
    print(timeit.default_timer() - start)


if __name__ == '__main__':
    import timeit

    print(timeit.timeit(main, number=1))

