import numpy as np
from matplotlib.pyplot import plot

SIZE = 4
iters = 100


def generate_prob_seq(size):
    values = [np.random.randint(1, 100) for _ in range(size)]
    values = [v / sum(values) for v in values]
    return values


def get_initial_state():
    return generate_prob_seq(SIZE)


def get_transition_matrix():
    return [generate_prob_seq(SIZE) for _ in range(SIZE)]


def get_result(P, p0):
    P = P.T
    P = P - np.identity(SIZE)
    P[-1] = np.ones(SIZE)
    return np.linalg.solve(P, p0.T)


def transition(P, p0, n=1):
    p = p0
    for _ in range(n):
        p = p @ P
    return p


def round_seq(p, e):
    return [round(v, e) for v in p]


def main():
    # p0 = get_initial_state()
    # p = get_transition_matrix()

    p = np.array([0, 0, 0, 1])
    P = np.array(
        [[0.8, 0.2, 0, 0], [0, 0.5, 0.5, 0], [0.3, 0, 0, 0.7], [0, 0.4, 0, 0.6]]
    )
    solution = get_result(P, p)  # аналитическое решение
    stds = []
    for i in range(iters):
        pn = p @ P
        std = np.std(pn - p)
        stds.append(std)
        p = pn

    print(p)
    print(solution)
    print(stds)
    plot(stds)


if __name__ == "__main__":
    main()
