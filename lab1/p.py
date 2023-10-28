import json
from pathlib import Path
import numpy as np


def parse_json(content: str):
    doc = json.loads(content)
    C = set()
    constraints = doc["constraints"]
    height = len(constraints)
    width = len(constraints[0]["coefs"])

    f = np.array(doc["f"])

    if doc["goal"] == "min":
        f *= -1

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

    return A, B[0], f, C


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
        pivot_row = 0
        for i, v in enumerate(tableau[:-1, -1]):
            if v < 0:
                pivot_row = i
                break

        for i, v in enumerate(tableau[pivot_row][:-1]):
            if v < 0:
                return pivot_row, i

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


def solve(A, b, c, C):
    tableau = make_tableau(A, b, c, C)

    height = len(A)
    width = len(c)

    optimal = False
    feasible = True

    while feasible and not optimal:
        # for i in range(5):
        pivot_row, pivot_column = get_pivot(tableau)
        if pivot_column is None:
            feasible = False
            print("unbounded")
            break
        elif pivot_column == -1:
            feasible = False
            print("infeasible")
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

        solutions = tableau[:, -1]

        optimal = np.all(tableau[-1][:-1] >= 0)

    if optimal:
        solutions = np.zeros(width)
        has_solution = False
        for i in range(width):
            if sum(tableau[:, i]) != 1:
                solutions[i] = 0
            else:
                has_solution = True
                solutions[i] = tableau[tableau[:, i].argmax(), -1]
        value = tableau[-1, -1]
        if has_solution:
            print(tableau, solutions, value)
        else:
            print("infeasible")


def main():
    path = Path("./assets/input7.json")
    content = from_file(path)
    A, b, c, C = parse_json(content)
    solve(A=A, b=b, c=c, C=C)


main()
