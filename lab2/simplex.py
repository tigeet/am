import json
from pathlib import Path
import numpy as np

with_log = False


def parse_json(content: str):
    doc = json.loads(content)
    C = set()
    constraints = doc["constraints"]
    height = len(constraints)
    width = len(constraints[0]["coefs"])

    f = np.array(doc["f"])
    is_min = False
    if doc["goal"] == "min":
        f *= -1
        is_min = True

    A = np.empty(0)
    B = np.empty(0)

    for i, constraint in enumerate(constraints):
        row_len = len(constraint["coefs"])

        coefs = np.zeros(width)
        coefs[:row_len] = np.array(constraint["coefs"])

        b = constraint["b"]

        if constraint["type"][0:2] == "gt":
            b = -b
            coefs *= -1
        if constraint["type"][0:2] == "eq":
            C.add(i)
        A = np.append(A, coefs)
        B = np.append(B, b)

    A = np.reshape(A, (height, width))
    B = np.reshape(B, (1, height))

    return A, B[0], f, C, is_min


def from_file(path: Path):
    file = open(path.absolute(), "r", encoding="utf-8")
    content = file.read()
    file.close()
    return content


def make_tableau(A, b, c, C):
    tableau = np.vstack((A, -c))

    identity = np.identity(tableau.shape[0])
    for i, _ in enumerate(identity):
        if i in C:
            identity[i][i] = 0

    tableau = np.hstack((tableau, identity))
    b = np.append(b, 0)
    tableau = np.hstack((tableau, np.atleast_2d(b).T))

    return tableau


def get_pivot(tableau):
    if np.any(tableau[:-1, -1] < 0):
        target_row = 0
        for i, v in enumerate(tableau[:-1, -1]):
            if v < 0:
                target_row = i
                break

        pivot_col = None
        for i, v in enumerate(tableau[target_row]):
            if v < 0:
                pivot_col = i
                break

        if pivot_col is None:
            return -1, -1

        f = tableau[:-1, -1] / tableau[:-1, pivot_col]
        f = [v if v > 0 else np.inf for v in f]
        pivot_row = np.argmin(f)
        if f[pivot_row] == np.inf:
            return -1, -1
        return pivot_row, pivot_col
        # for i, v in enumerate(tableau[pivot_row][:-1]):
        #     if v < 0:
        #         return pivot_row, i

        return -1, -1
    else:
        height = len(tableau - 1)
        pivot_column = np.argmin(tableau[-1][:-1])
        nonneg = [i for i in range(0, height) if tableau[i, pivot_column] > 0]
        if len(nonneg) == 0:
            return None, None

        division = [tableau[i][-1] / tableau[i][pivot_column] for i in nonneg]
        pivot_row = nonneg[division.index(min(division))]
        return pivot_row, pivot_column


def solve(A, b, c, C=set(), is_min=False):
    tableau = make_tableau(A, b, c, C)
    if with_log:
        print(tableau, "\n------")
    # print(tableau)
    height = len(A)
    width = len(c)

    optimal = False
    feasible = True

    while feasible and not optimal:
        # for i in range(5):
        pivot_row, pivot_column = get_pivot(tableau)
        if pivot_column is None:
            feasible = False
            # print("unbounded")
            break
        elif pivot_column == -1:
            feasible = False
            # print("infeasible")
            break

        tableau[pivot_row] /= tableau[pivot_row][pivot_column]

        for i in range(height + 1):
            if i == pivot_row:
                continue
            tableau[i] -= (
                tableau[i][pivot_column]
                * tableau[pivot_row]
                / tableau[pivot_row][pivot_column]
            )
        if with_log:
            print(tableau, "\n------")
        solutions = tableau[:, -1]

        optimal = np.all(tableau[:-1, -1] >= 0) and np.all(tableau[-1][:-1] >= 0)

    if optimal:
        solutions = np.zeros(width)
        has_solution = False
        for i in range(width):
            if sum(tableau[:, i]) != 1:
                solutions[i] = 0
            else:
                has_solution = True
                solutions[i] = tableau[tableau[:, i].argmax(), -1]
        if has_solution:
            if with_log:
                print("Simplex solution:", solutions, value)
            value = c @ solutions
            if is_min:
                value = -value
            return solutions, value
    raise "no solution"


def main():
    # path = Path("./assets/input7.json")
    # content = from_file(path)
    # A, b, c, C, is_min = parse_json(content)

    A = np.array([[1, 1], [-2, 3]])
    b = np.array([13, -6])
    c = np.array([1, 2])

    is_min = False
    # A = np.array(
    #     [
    #         [
    #             -1,
    #             -1,
    #         ],
    #         [-1, -2],
    #         [-5, 1],
    #     ]
    # )
    # b = np.array([-20, -25, 4])
    # c = np.array([-3, -4])
    C = set([0])
    solution, value = solve(A=A, b=b, c=c, C=C, is_min=is_min)

    print(solution, value)


if __name__ == "__main__":
    main()
