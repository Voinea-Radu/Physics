from prettytable import PrettyTable
from unum import Unum
from unum.units import s, min, A, T, eV

from utils import delete_file
from utils import write_to_csv

imp = Unum.unit("imp")
mT = Unum.unit("mT", T / 1000)
keV = Unum.unit("keV", T * eV)

F = 0 * imp  # Background count
t_background = 10 * min
f = F / t_background

t_measurement = 60 * s


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
        self.B = B
        self.E = E
        self.N = N
        self.n_prime = N / t_measurement
        self.n = self.n_prime - f
        self.sigma_n = ((self.n / t_measurement) + f / t_background) ** 1 / 2


sr_90: list[Data] = [
    Data(0 * A, 4.4 * mT, 5.47459 * keV, 0 * imp),
    Data(0.1 * A, 15.4 * mT, 21.56079 * keV, 0 * imp),
    Data(0.2 * A, 24.5 * mT, 47.34219 * keV, 0 * imp),
    Data(0.3 * A, 34.7 * mT, 81.55464 * keV, 0 * imp),
    Data(0.4 * A, 45.7 * mT, 122.83436 * keV, 0 * imp),
    Data(0.5 * A, 56.1 * mT, 169.8972 * keV, 0 * imp),
    Data(0.6 * A, 65.8 * mT, 221.62951 * keV, 0 * imp),
    Data(0.7 * A, 78.0 * mT, 277.1123 * keV, 0 * imp),
    Data(0.8 * A, 87.0 * mT, 335.60853 * keV, 0 * imp),
    Data(0.9 * A, 97.4 * mT, 396.53567 * keV, 0 * imp),
    Data(1.0 * A, 107.4 * mT, 459.43598 * keV, 0 * imp),
    Data(1.1 * A, 120.2 * mT, 523.94976 * keV, 0 * imp),
    Data(1.2 * A, 128.5 * mT, 589.79335 * keV, 0 * imp),
    Data(1.3 * A, 140.0 * mT, 656.74184 * keV, 0 * imp),
    Data(1.4 * A, 149.0 * mT, 724.61564 * keV, 0 * imp),
    Data(1.5 * A, 159.3 * mT, 793.27029 * keV, 0 * imp),
    Data(1.6 * A, 168.1 * mT, 862.58873 * keV, 0 * imp),
    Data(1.7 * A, 174.7 * mT, 932.47532 * keV, 0 * imp),
]

na_20: list[Data] = [
    Data(0 * A, 4.4 * mT, 5.47459 * keV, 0 * imp),
    Data(0.1 * A, 15.4 * mT, 21.56079 * keV, 0 * imp),
    Data(0.2 * A, 24.5 * mT, 47.34219 * keV, 0 * imp),
    Data(0.3 * A, 34.7 * mT, 81.55464 * keV, 0 * imp),
    Data(0.4 * A, 45.7 * mT, 122.83436 * keV, 0 * imp),
    Data(0.5 * A, 56.1 * mT, 169.8972 * keV, 0 * imp),
    Data(0.6 * A, 65.8 * mT, 221.62951 * keV, 0 * imp),
    Data(0.7 * A, 78.0 * mT, 277.1123 * keV, 0 * imp),
    Data(0.8 * A, 87.0 * mT, 335.60853 * keV, 0 * imp),
    Data(0.9 * A, 97.4 * mT, 396.53567 * keV, 0 * imp),
    Data(1.0 * A, 107.4 * mT, 459.43598 * keV, 0 * imp),
    Data(1.1 * A, 120.2 * mT, 523.94976 * keV, 0 * imp),
    Data(1.2 * A, 128.5 * mT, 589.79335 * keV, 0 * imp),
    Data(1.3 * A, 140.0 * mT, 656.74184 * keV, 0 * imp),
    Data(1.4 * A, 149.0 * mT, 724.61564 * keV, 0 * imp),
    Data(1.5 * A, 159.3 * mT, 793.27029 * keV, 0 * imp),
    Data(1.6 * A, 168.1 * mT, 862.58873 * keV, 0 * imp),
    Data(1.7 * A, 174.7 * mT, 932.47532 * keV, 0 * imp),
]


def main():
    sr_90_table = PrettyTable()
    na_20_table = PrettyTable()

    sr_90_table.field_names = ["Nr. Crt", "I (A)", "B (mT)", "N (imp)", "n'=N/t", "n=n'-f", "sigma_n"]
    na_20_table.field_names = ["Nr. Crt", "I (A)", "B (mT)", "N (imp)", "n'=N/t", "n=n'-f", "sigma_n"]

    for index, data in enumerate(sr_90):
        sr_90_table.add_row(
            [
                index + 1,
                data.I,
                data.B,
                data.N,
                data.n_prime,
                data.n,
                data.sigma_n,
            ]
        )

    for index, data in enumerate(na_20):
        na_20_table.add_row(
            [
                index + 1,
                data.I,
                data.B,
                data.N,
                data.n_prime,
                data.n,
                data.sigma_n,
            ]
        )

    write_to_csv("sr_90_table.csv", sr_90_table)
    write_to_csv("na_20_table.csv", na_20_table)


if __name__ == "__main__":
    delete_file("results.txt")
    main()
