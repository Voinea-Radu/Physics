from cmath import e, pi

from numpy.ma.core import append
from prettytable import PrettyTable
from unum import Unum
from unum.units import s, min, A, T, eV

from utils import append_to_file
from utils import delete_file
from utils import write_to_csv


class Data:
    n: int
    k_exp: int
    nk_exp: int
    P: int
    k_th_P: int
    P_G: int
    k_th_G: int

    def __init__(self, n: int, k_exp: int):
        self.n = n
        self.k_exp = k_exp
        self.nk_exp = n * k_exp
        self.P = 0
        self.k_th_P = 0
        self.P_G = 0
        self.k_th_G = 0


data: list[Data] = [
    Data(0, 0),
    Data(1, 0),
    Data(2, 0),
    Data(3, 0),
    Data(4, 0),
    Data(5, 0),
    Data(6, 0),
    Data(7, 0),
    Data(8, 0),
    Data(9, 0),
    Data(10, 0),
    Data(11, 0),
    Data(12, 0),
    Data(13, 0),
    Data(14, 0),
    Data(15, 0),
]


def main():
    N = sum([d.k_exp for d in data])
    sigma = sum([d.nk_exp for d in data])
    a = N / sigma
    n_med = sum(range(1, len(data))) / len(data)

    data[0].P = e / N
    for index, d in enumerate(data[1:]):
        d.P = data[index].P * a / (index + 1)

    for d in data:
        d.k_th_P = d.P * d.k_exp

    for index, d in enumerate(data):
        d.P_G = 1 / ((2 * pi) ** (1 / 2) * N / n_med) * e ** (-(index - n_med) ** 2 / (2 * n_med))
        d.k_th_G = d.P_G * d.k_exp

    table = PrettyTable()
    table.field_names = ["n", "k_exp", "nk_exp", "P", "k_th_P", "P_G", "k_th_G"]
    for d in data:
        table.add_row([d.n, d.k_exp, d.nk_exp, d.P, d.k_th_P, d.P_G, d.k_th_G])

    write_to_csv("results.txt", table)


if __name__ == "__main__":
    delete_file("results.txt")
    main()
