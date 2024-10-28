import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
from scipy.stats import linregress

from src.utils import write_to_csv

times = np.array([600, 300, 300, 300])
distances = np.array([np.inf, 10, 20, 30])  # TODO Change
counts = np.array([100, 1200, 800, 600])  # TODO Change

measurement_time = 300
background_time = 600
background_count = 100
epsilon = 0.2
S = 2
tau = 10 ** -6
D = 2


def method_1(times, distances, counts):
    sigma_N = [N ** (1 / 2) for N in counts]
    n_prime = [N / t for N, t in zip(counts, times)]
    sigma_n_prime = [sigma / t for sigma, t in zip(sigma_N, times)]
    n_double_prime = [n_p / (1 - tau * n) for n_p, n in zip(n_prime, counts)]
    sigma_n_double_prime = [sigma_n_p / (1 - tau * n) for sigma_n_p, n in zip(sigma_n_prime, counts)]
    n = [n_dp - n_prime[0] for n_dp in n_double_prime]
    sigma_n = [(sigma_dp ** 2 + sigma_n_prime[0] ** 2) ** (1 / 2) for sigma_dp in sigma_n_double_prime]

    table = PrettyTable()

    table.add_column("r (cm)", distances)
    table.add_column("t (s)", times)
    table.add_column("N", counts)
    table.add_column("sigma_N", sigma_N)
    table.add_column("n'", n_prime)
    table.add_column("sigma_n'", sigma_n_prime)
    table.add_column("n''", n_double_prime)
    table.add_column("sigma_n''", sigma_n_double_prime)
    table.add_column("n", n)
    table.add_column("sigma_n", sigma_n)

    write_to_csv("method_1.csv", table)

    counts = counts[1:]
    distances = distances[1:]

    n_fond = background_count / background_time
    n_values = counts / measurement_time - n_fond

    plt.figure()
    plt.plot(distances, n_values, 'o-', label='Date experimentale')
    plt.xlabel("Distanța (cm)")
    plt.ylabel("Număr impulsuri (corectate)")
    plt.title("Graficul n = f(r)")
    plt.legend()
    plt.show()

    slope, intercept, _, _, _ = linregress(distances, n_values)
    n_extrapolated = intercept
    activity = n_extrapolated / (S * epsilon)
    print(f"Activitatea absolută estimată (Metoda 1): {activity:.2f} Bq")


def method_2(times, distances, counts):
    omega_over_4pi = [0 if r == np.inf else (1 / (4 * np.pi)) * (1 - 1 / (1 + (D / (2 * r)) ** 2)) for r in distances]
    sigma_N = [N ** (1 / 2) for N in counts]
    n_prime = [N / t for N, t in zip(counts, times)]
    sigma_n_prime = [sigma / t for sigma, t in zip(sigma_N, times)]
    n_double_prime = [n_p / (1 - tau * n) for n_p, n in zip(n_prime, counts)]
    sigma_n_double_prime = [sigma_n_p / (1 - tau * n) for sigma_n_p, n in zip(sigma_n_prime, counts)]
    n = [n_dp - n_prime[0] for n_dp in n_double_prime]
    sigma_n = [(sigma_dp ** 2 + sigma_n_prime[0] ** 2) ** (1 / 2) for sigma_dp in sigma_n_double_prime]

    table = PrettyTable()

    table.add_column("r (cm)", distances)
    table.add_column("omega / 4pi", [f"{omega:.6f}" for omega in omega_over_4pi])
    table.add_column("t (s)", times)
    table.add_column("N", counts)
    table.add_column("sigma_N", sigma_N)
    table.add_column("n'", n_prime)
    table.add_column("sigma_n'", sigma_n_prime)
    table.add_column("n''", n_double_prime)
    table.add_column("sigma_n''", sigma_n_double_prime)
    table.add_column("n", n)
    table.add_column("sigma_n", sigma_n)

    write_to_csv("method_2.csv", table)

    counts = counts[1:]
    distances = distances[1:]

    n_fond = background_count / background_time
    n_prime = [(count / measurement_time) - n_fond for count in counts]
    omega_over_4pi = [(1 / (4 * np.pi)) * (1 - 1 / (1 + (D / (2 * r)) ** 2)) for r in distances]

    four_pi_over_omega = [4 / omega if omega != 0 else np.nan for omega in omega_over_4pi]
    n_prime_corrected = [n / omega if omega != 0 else np.nan for n, omega in zip(n_prime, omega_over_4pi)]

    plt.figure()
    plt.plot(four_pi_over_omega, n_prime_corrected, 'o-', label="4π/Ω vs n' corectat")
    plt.xlabel("4π/Ω (corecție unghi solid)")
    plt.ylabel("n' corectat (imp/s)")
    plt.title("Graficul 4π/Ω vs n' corectat")
    plt.legend()
    plt.show()

    slope, intercept, _, _, _ = linregress(four_pi_over_omega, n_prime_corrected)

    activity2 = slope / (epsilon * S)
    print(f"Activitatea absolută estimată (Metoda 2): {activity2:.2f} Bq")


def main():
    method_1(times, distances, counts)
    method_2(times, distances, counts)


if __name__ == "__main__":
    main()
