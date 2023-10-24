import numpy as np

# c = np.array([-1])
# A = np.array([[-1]])
# b = np.array([-5])

c = np.array([1, -1])
A = np.array([[1, 0], [0, -1]])
b = np.array([5, -5])

# c = np.array([7, 6])
# A = np.array([[2, 4], [3, 2]])
# b = np.array([16, 12])


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


def main():
    # c = np.array([3, 2, 4])
    # A = np.array([[3, 2, 5], [4, 2, 3], [-2, -1, -1]])
    # b = np.array([18, 16, -4])

    c = np.array([-3, -4])
    A = np.array([[-1, -1], [-1, -2], [-5, 1]])
    b = np.array([-20, -25, 4])

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


main()
