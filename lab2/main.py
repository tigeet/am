import numpy as np
from simplex import solve
from pathlib import Path
import json


def simplify_rows(A):
    A = A.copy()

    def helper():
        for i, _ in enumerate(A):
            for j, _ in enumerate(A):
                if i == j:
                    continue

                if np.all(A[i] >= A[j]):
                    return True, np.delete(A, j, axis=0)
        return False, A

    can_be_simplified = True
    while can_be_simplified:
        can_be_simplified, A = helper()
    return A


def simplify_cols(A):
    A = A.copy()

    def helper(A):
        for i, _ in enumerate(A[0]):
            for j, _ in enumerate(A[0]):
                if i == j:
                    continue

                if np.all(A[:, i] <= A[:, j]):
                    return True, np.delete(A, j, axis=1)
        return False, A

    can_be_simplified = True

    while can_be_simplified:
        can_be_simplified, A = helper(A)

    return A


def simplify(A):
    A = simplify_rows(A)
    A = simplify_cols(A)
    return A


def boundary(A):
    l = max([min(row) for row in A])
    u = min([max(col) for col in A.T])

    return l, u


def from_json(path: Path):
    file = open(path.absolute(), "r", encoding="utf-8")
    content = file.read()
    content = json.loads(content)
    a = content["matrix"]

    _json = [[float(c) for c in row] for row in a]

    file.close()
    return np.array(_json)


def resize(arr, ln):
    return arr + [0] * (ln - len(arr))


def find_saddle_point(A):
    for i, _ in enumerate(A):
        for j, _ in enumerate(A.T):
            if A[i][j] == min(A[i]) and A[i][j] == max(A[:, j]):
                return i, j


def main():
    path = Path("./assets/input4.json")
    A = from_json(path)

    # A = [[2, 5, 8], [7, 4, 3]]  # решение 4.5, A = [0.5, 0.5], B = [0.17, 0.83]

    # A = [
    # [1, 4, 6, 3, 7],
    # [3, 1, 2, 4, 3],
    # [2, 3, 4, 3, 5],
    # [0, 1, 5, 2, 6],
    # ]  # v = 7/3, A = [2/3, 1/3, 0, 0, 0], B = [0, 1/3, 2/3, 0]

    # A = [
    #     [4, 2, 3, -1],
    #     [-4, 0, -2, 2],
    # ]  # v = 4/11, A = [6/11, 5/11], B = [3/11, 0, 0 ,8/11]

    A = np.array(A)
    len_a = len(A)
    len_b = len(A[0])

    a = simplify(A)

    l, u = boundary(a)
    if l == u:
        l0, l1 = find_saddle_point(A)
        print("Игра имеет решение в чистых стратегиях")
        print(f"Цена игры = {u}")
        print(f"Оптимальная стратегия игрока A: №{l0 + 1}")
        print(f"Оптимальная стратегия игрока B: №{l1 + 1}")
        return

    b = np.ones(len(a)).T
    c = np.ones(len(a[0]))

    solution_b, value_b = solve(a, b, c)
    solution_b = [y / value_b for y in solution_b]
    value = 1 / value_b

    a = -a.T
    b = -np.ones(len(a)).T
    c = -np.ones(len(a[0]))

    solution_a, value_a = solve(a, b, c, is_min=True)

    solution_a = [x / value_a for x in solution_a]

    solution_a = resize(solution_a, len_a)
    solution_b = resize(solution_b, len_b)

    print(f"{l} < v < {u}")
    print(f"Цена игры = {value}")
    print(f"Стратегии игрока A = {[str(round(x, 2)) for x in solution_a]}")
    print(f"Стратегии игрока B = {[str(round(y, 2)) for y in solution_b]}")
    print("")
    print(f"Стратегии игрока A = {[str(x) for x in solution_a]}")
    print(f"Стратегии игрока B = {[str(y) for y in solution_b]}")


main()
