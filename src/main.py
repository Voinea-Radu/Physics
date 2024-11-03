import numpy as np
from matplotlib import pyplot as plt
from unum.units import cm, s, m

from utils import append_to_file, delete_file

times = [120] * 6
distances = [3.5, 4, 4.5, 5, 5.5, 6]

background_time = 600
background_count = 1682

S = 0.85
D = 4.2


def main():
    # omega_over_4pi = [1 / 2 - 1 / (4 + (D / x) ** 2) ** (1 / 2) for x in distances]
    omega_over_4pi = [D ** 2 / (16 * x ** 2) for x in distances]
    # omega_over_4pi = [D**2/(16*x**2) for x in distances]
    counts = [72801, 66339, 61802, 55168, 52768, 47245]
    counts = [count / time for count, time in zip(counts, times)]
    print(counts)

    slope, intercept = np.polyfit(omega_over_4pi, counts, 1)
    pred = slope * np.array(omega_over_4pi) + intercept

    plt.scatter(omega_over_4pi, counts)
    plt.plot(omega_over_4pi, pred, color="red", label=f"Linear Fit: y = {slope:.2f}x + {intercept:.2f}")
    plt.show()
    plt.savefig("results.png")
    epsilon = slope / (220_000 * 0.85)

    append_to_file("results.txt", f"epsilon = {epsilon*100:.2f}%")


if __name__ == "__main__":
    delete_file("results.txt")
    main()
