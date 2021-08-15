import level
from display import display_sudoku
from solve import solve_sudoku


def main():
    with open(level.HARD, "r") as f:
        matrix = [list(map(lambda x: int(x) if x.isdigit() else set(), line)) for line in map(str.strip, f.readlines())]

    solve_sudoku(matrix)

    k = 3
    resolution = (210 * k, 210 * k)
    display_sudoku(matrix, resolution)


def time_main():
    import timeit

    start = timeit.default_timer()
    main()
    print(timeit.default_timer() - start)


if __name__ == '__main__':
    time_main()
