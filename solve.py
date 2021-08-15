SIDE = 9
SQUARES_ON_SIDE = 9 // 3
FULL = set(range(1, 10))


def solve_sudoku(matrix):
    while difference(matrix) or elimination(matrix):
        pass


def difference(matrix) -> bool:
    flag = False
    squares, horizontals, verticals = get_fills(matrix)
    for y in range(SIDE):
        for x in range(SIDE):
            if type(matrix[y][x]) == set:
                new = FULL - squares[y // 3][x // 3] - horizontals[y] - verticals[x]
                # print()
                # print(squares[y // 3][x // 3], horizontals[y], verticals[x])
                if len(new) > 1:
                    matrix[y][x] = new
                else:
                    matrix[y][x] = new.pop()
                    flag = True
    return flag


def elimination(matrix) -> bool:
    flag = False
    squares, horizontals, verticals = get_possibles(matrix)

    sp, hp, vp = get_predictions(matrix)
    used = set()
    for y in range(SIDE):
        for x in range(SIDE):
            if type(array := matrix[y][x]) == set:
                for value in array:
                    if squares[y // 3][x // 3][value] == 1 or \
                            horizontals[y][value] == 1 or \
                            verticals[x][value] == 1:
                        matrix[y][x] = value
                        flag = True
                        break
    return flag


def get_fills(matrix):
    squares = tuple(tuple(set() for _ in range(SQUARES_ON_SIDE)) for _ in range(SQUARES_ON_SIDE))
    horizontals = tuple(set() for _ in range(SIDE))
    verticals = tuple(set() for _ in range(SIDE))
    for y in range(SIDE):
        for x in range(SIDE):
            if type(value := matrix[y][x]) == int:
                squares[y // 3][x // 3].add(value)
                horizontals[y].add(value)
                verticals[x].add(value)
    return squares, horizontals, verticals


def get_possibles(matrix):
    squares = tuple(tuple(dict() for _ in range(SQUARES_ON_SIDE)) for _ in range(SQUARES_ON_SIDE))
    horizontals = tuple(dict() for _ in range(SIDE))
    verticals = tuple(dict() for _ in range(SIDE))
    for y in range(SIDE):
        for x in range(SIDE):
            if type(array := matrix[y][x]) == set:
                for value in array:
                    squares[y // 3][x // 3][value] = squares[y // 3][x // 3].get(value, 0) + 1
                    horizontals[y][value] = horizontals[y].get(value, 0) + 1
                    verticals[x][value] = verticals[x].get(value, 0) + 1
    return squares, horizontals, verticals


def get_predictions(matrix):
    squares = tuple(tuple(list() for _ in range(SQUARES_ON_SIDE)) for _ in range(SQUARES_ON_SIDE))
    horizontals = tuple(list() for _ in range(SIDE))
    verticals = tuple(list() for _ in range(SIDE))
    for y in range(SIDE):
        for x in range(SIDE):
            if type(array := matrix[y][x]) == set:
                squares[y // 3][x // 3].append(array)
                horizontals[y].append(array)
                verticals[x].append(array)
    return squares, horizontals, verticals


def general_coords(x, y):
    for i in range(SIDE):
        yield x, i
        yield i, y
