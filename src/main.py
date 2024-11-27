from prettytable import PrettyTable
from unum import Unum
from unum.units import s, min, A, T, eV

from utils import delete_file
from utils import write_to_csv

imp = Unum.unit("imp")
mT = Unum.unit("mT", T / 1000)
keV = Unum.unit("keV", T * eV)

F = 116 * imp  # Background count
t_background = 10 * min
f = F / t_background

t_measurement = 60 * s

magnet_data = [
    (0, 15.8),
    (0.2, 34),
    (0.2, 34),
    (0.22, 33.4),
    (0.28, 38.8),
    (0.3, 42),
    (0.3, 41.2),
    (0.3, 42),
    (0.34, 45.1),
    (0.4, 50.6),
    (0.4, 50.6),
    (0.43, 53.4),
    (0.5, 61.7),
    (0.5, 61.5),
    (0.5, 61.7),
    (0.54, 65.7),
    (0.58, 70.5),
    (0.6, 71.5),
    (0.6, 71.7),
    (0.6, 71.5),
    (0.63, 75.3),
    (0.65, 76.1),
    (0.65, 78.8),
    (0.65, 76.1),
    (0.7, 82.2),
    (0.7, 82.2),
    (0.71, 84.6),
    (0.74, 87.8),
    (0.75, 89),
    (0.75, 89),
    (0.77, 90.7),
    (0.8, 93.6),
    (0.8, 93.6),
    (0.81, 93),
    (0.84, 97),
    (0.85, 102),
    (0.85, 100),
    (0.85, 102),
    (0.89, 102),
    (0.9, 106),
    (0.9, 106),
    (0.93, 107),
    (0.95, 110),
    (0.95, 110),
    (1, 113),
    (1, 113),
    (1.03, 117),
    (1.09, 123),
    (1.1, 125),
    (1.18, 133),
    (1.21, 133),
    (1.21, 133),
    (1.24, 139),
    (1.28, 143),
    (1.33, 148),
    (1.38, 152),
    (1.4, 152),
    (1.4, 152),
    (1.43, 157),
    (1.45, 163),
    (1.5, 167),
    (1.57, 172),
    (1.6, 174),
    (1.6, 174),
    (1.63, 177),
    (1.68, 181),
    (1.7, 190),
    (1.74, 189),
    (1.8, 190),
    (1.8, 191),
    (1.8, 190),
    (1.8, 187),
    (1.84, 196),
    (1.9, 201),
    (1.9, 205),
    (1.97, 209),
    (2, 206),
    (2, 206),
    (2.01, 212),
    (2.1, 216),
    (2.2, 221),
    (2.2, 221),
]


def find_intermediary_point(data: list[tuple[float, float]], x: float) -> float:
    from scipy.interpolate import interp1d

    # Extract x and y values from the data
    x_values, y_values = zip(*data)

    # Create a linear interpolation function
    interpolation_function = interp1d(x_values, y_values, kind='linear', fill_value='extrapolate')

    # Compute the y value for the given x
    y = interpolation_function(x)

    return y


class Data:
    I: Unum
    B: Unum
    E: Unum
    N: Unum
    n_prime: Unum
    n: Unum
    sigma_n: Unum

    def __init__(self, I: Unum, B: Unum, E: Unum, N: Unum):
        self.I = I
        self.B = find_intermediary_point(data=magnet_data, x=I.asNumber()) * mT
        self.E = ((5/100* self.B.asNumber()/1000 * 300_000_000 / 1000) ** 2 + 511 ** 2) ** (1 / 2) - 511
        self.E *= keV
        self.N = N
        self.n_prime = N / t_measurement
        self.n = self.n_prime - f
        self.sigma_n = ((self.n / t_measurement) + f / t_background) ** 1 / 2


sr_90: list[Data] = [
    Data(0 * A, 4.4 * mT, 5.47459 * keV, 169 * imp),
    Data(0.133 * A, 4.4 * mT, 5.47459 * keV, 336 * imp),
    Data(0.208 * A, 4.4 * mT, 5.47459 * keV, 439 * imp),
    Data(0.256 * A, 4.4 * mT, 5.47459 * keV, 481 * imp),
    Data(0.308 * A, 4.4 * mT, 5.47459 * keV, 588 * imp),
    Data(0.401 * A, 4.4 * mT, 5.47459 * keV, 774 * imp),
    Data(0.444 * A, 4.4 * mT, 5.47459 * keV, 968 * imp),
    Data(0.494 * A, 4.4 * mT, 5.47459 * keV, 1049 * imp),
    Data(0.555 * A, 4.4 * mT, 5.47459 * keV, 1069 * imp),
    Data(0.585 * A, 4.4 * mT, 5.47459 * keV, 1049 * imp),
    Data(0.585 * A, 4.4 * mT, 5.47459 * keV, 1127 * imp),
    Data(0.707 * A, 4.4 * mT, 5.47459 * keV, 1234 * imp),
    Data(0.794 * A, 4.4 * mT, 5.47459 * keV, 1156 * imp),
    Data(0.899 * A, 4.4 * mT, 5.47459 * keV, 1124 * imp),
    Data(1.042 * A, 4.4 * mT, 5.47459 * keV, 834 * imp),
    Data(1.111 * A, 4.4 * mT, 5.47459 * keV, 810 * imp),
    Data(1.206 * A, 4.4 * mT, 5.47459 * keV, 663 * imp),
    Data(1.302 * A, 4.4 * mT, 5.47459 * keV, 585 * imp),
    Data(1.396 * A, 4.4 * mT, 5.47459 * keV, 453 * imp),
    Data(1.511 * A, 4.4 * mT, 5.47459 * keV, 340 * imp),
    Data(1.595 * A, 4.4 * mT, 5.47459 * keV, 293 * imp),
    Data(1.703 * A, 4.4 * mT, 5.47459 * keV, 195 * imp),
]

def main():
    sr_90_table = PrettyTable()

    sr_90_table.field_names = ["Nr. Crt", "I (A)", "B (mT)", "E (keV)", "N (imp)", "n'=N/t", "n=n'-f", "sigma_n"]

    for index, data in enumerate(sr_90):
        sr_90_table.add_row(
            [
                index + 1,
                data.I,
                data.B,
                data.E,
                data.N,
                data.n_prime,
                data.n,
                data.sigma_n,
            ]
        )

    # graph the sr_90 data
    import matplotlib.pyplot as plt
    import numpy as np

    x = [data.E.asNumber() for data in sr_90]
    y = [data.n.asNumber() for data in sr_90]

    plt.scatter(x, y)

    z = np.polyfit(x, y, 5)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--")

    # show the max of the p function
    max_p = 0
    max_x = 0
    for x in range(0,2500):
        if p(x) > max_p:
            max_p = p(x)
            max_x = x

    plt.plot(max_x, max_p, 'ro')
    print(f"max_x = {max_x}")
    print(f"max_p = {max_p}")

    plt.xlabel('I (A)')
    plt.ylabel('N (imp)')
    plt.title('Energie in functie de curent')
    plt.show()

    write_to_csv("sr_90_table.csv", sr_90_table)


if __name__ == "__main__":
    delete_file("results.txt")
    main()
