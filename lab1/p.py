import json
from pathlib import Path
import numpy as np


# c = np.array([1, -1])
# A = np.array([[1, 0], [0, -1]])
# b = np.array([5, -5])


def parse_json(content: str):
    doc = json.loads(content)

    constraints = doc["constraints"]
    height = len(constraints)
    width = len(constraints[0]["coefs"])

    print(width, height)

    f = np.array(doc["f"])

    if doc["goal"] == "min":
        f *= -1

    A = np.empty(0)
    b = np.empty(0)

    for i, constraint in enumerate(constraints):
        row_len = len(constraint["coefs"])

        coefs = np.zeros(width)
        coefs[:row_len] = np.array(constraint["coefs"])

        b = constraint["b"]

        if constraint["type"][0:2] == "gt":
            b = -b
            coefs *= -1

        A = np.append(A, coefs)
        b = np.append(b, b)

    A = np.reshape(A, (height, width))
    b = np.reshape(b, (1, height))

    return A, b[0], f


def from_file(path: Path):
    file = open(path.absolute(), "r", encoding="utf-8")
    content = file.read()
    file.close()
    return content


def make_tableau(A, b, c):
    tableau = np.vstack((A, -c))
    tableau = np.hstack((tableau, np.identity(tableau.shape[0])))
    b = np.append(b, 0)
    tableau = np.hstack((tableau, np.atleast_2d(b).T))

    # width = len(A[0])
    # tableau = np.hstack((A, np.identity(A.shape[0])))

    # b = np.transpose(b)
    # tableau = np.hstack((tableau, np.atleast_2d(b).T))

    # # for i, v in enumerate(b):
    # #     if v < 0:
    # #         tableau[i] *= -1

    # c *= -1
    # c = np.append(c, np.zeros(len(tableau[0]) - len(c)))
    # tableau = np.vstack((tableau, c))

    return tableau


def get_pivot(tableau):
    if np.any(tableau[:-1, -1] < 0):
        pivot_row = 0
        for i, v in enumerate(tableau[:-1, -1]):
            if v < 0:
                pivot_row = i
                break

        pivot_column = 0
        for i, v in enumerate(tableau[pivot_row][:-1]):
            if v < 0:
                pivot_column = i

                break
        print(pivot_row, pivot_column)
        return pivot_row, pivot_column
    else:
        height = len(tableau - 1)
        pivot_column = np.argmin(tableau[-1][:-1])
        # print("pc", pivot_column, tableau[:-1, -1])
        nonneg = [i for i in range(0, height) if tableau[i, pivot_column] > 0]
        if len(nonneg) == 0:
            return None, None

        division = [tableau[i][-1] / tableau[i][pivot_column] for i in nonneg]
        print(division)
        pivot_row = nonneg[division.index(min(division))]
        return pivot_row, pivot_column


def solve(A, b, c):
    tableau = make_tableau(A, b, c)

    height = len(A)
    width = len(c)

    optimal = False
    feasible = True

    print(tableau, end="\n\n")

    while feasible and not optimal:
        # for i in range(5):
        pivot_row, pivot_column = get_pivot(tableau)
        if pivot_column is None:
            feasible = False
            break
        print(pivot_row, pivot_column)

        tableau[pivot_row] /= tableau[pivot_row][pivot_column]

        for i in range(height + 1):
            if i == pivot_row:
                continue
            tableau[i] -= (
                tableau[i][pivot_column]
                * tableau[pivot_row]
                / tableau[pivot_row][pivot_column]
            )

        solutions = tableau[:, -1]

        optimal = np.all(tableau[-1][:-1] >= 0)
        print(tableau, end="\n\n")

    if optimal:
        solutions = np.zeros(width)
        for i in range(width):
            if sum(tableau[:, i]) != 1:
                solutions[i] = 0
            else:
                solutions[i] = tableau[tableau[:, i].argmax(), -1]
        value = tableau[-1, -1]

        print(solutions, value)


def main():
    path = Path("./assets/input2.json")
    content = from_file(path)
    A, b, c = parse_json(content)
    solve(A=A, b=b, c=c)


main()
