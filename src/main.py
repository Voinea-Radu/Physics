from cmath import e, pi
from tkinter import N

import numpy as np
from matplotlib import pyplot as plt
from numpy.ma.core import append
from prettytable import PrettyTable
from unum import Unum
from unum.units import s, min, A, T, eV, cm, V, N, m

from src.utils import Median
from utils import append_to_file
from utils import delete_file
from utils import write_to_csv

R = 0.2 * m
n = 154
miu_0 = 4 * pi * 10 ** -7 * N * A ** -2


class Data1:
    r: Unum
    U: Unum
    I_1: Unum
    I_2: Unum
    I_3: Unum
    I_4: Unum
    I_5: Unum
    I_m: Unum
    sigma_I_m: Unum
    epsilon_I_m: Unum
    B: Unum
    e_over_m: Unum

    def __init__(self, r: Unum, U: Unum, I_1: Unum, I_2: Unum, I_3: Unum, I_4: Unum, I_5: Unum):
        self.r = r
        self.U = U
        self.I_1 = I_1
        self.I_2 = I_2
        self.I_3 = I_3
        self.I_4 = I_4
        self.I_5 = I_5
        median = Median([I_1, I_2, I_3, I_4, I_5])
        self.I_m = median.median
        self.sigma_I_m = median.square_deviation
        self.epsilon_I_m = self.sigma_I_m / self.I_m
        self.B = (4 / 5) ** (3 / 2) * miu_0 * n * self.I_m / R
        self.e_over_m = 2 * U / (r ** 2 * self.B ** 2)


data1: list[Data1] = [
    Data1(4 * cm, 185 * V, 1.573 * A, 1.574 * A, 1.566 * A, 1.563 * A, 1.561 * A),
]


class Data:
    r: Unum
    U: Unum
    I: Unum
    e_over_m: Unum

    def __init__(self, r: Unum, U: Unum, I: Unum):
        self.r = r
        self.U = U
        self.I = I
        term_1 = (125 / 32)
        term_2_1 = R ** 2
        term_2_2 = miu_0 ** 2 * n ** 2
        term_2 = term_2_1 / term_2_2
        term_3 = (U / (r ** 2 * I ** 2))
        self.e_over_m = term_1 * term_2 * term_3


data2: list[Data] = [
    None,
    None,
    None,
    Data(5 * cm, 180 * V, 1.238 * A),
    Data(5 * cm, 200 * V, 1.328 * A),
    Data(5 * cm, 220 * V, 1.398 * A),
    Data(5 * cm, 240 * V, 1.470 * A),
    Data(5 * cm, 260 * V, 1.528 * A),
    Data(5 * cm, 280 * V, 1.627 * A),
    Data(5 * cm, 300 * V, 1.685 * A),

    Data(4 * cm, 120 * V, 0.135 * A),
    Data(4 * cm, 140 * V, 0.162 * A),
    Data(4 * cm, 160 * V, 0.192 * A),
    Data(4 * cm, 180 * V, 1.503 * A),
    Data(4 * cm, 200 * V, 1.673 * A),
    Data(4 * cm, 220 * V, 1.764 * A),
    Data(4 * cm, 240 * V, 1.854 * A),
    Data(4 * cm, 260 * V, 1.937 * A),
    Data(4 * cm, 280 * V, 1.975 * A),
    Data(4 * cm, 300 * V, 2.118 * A),

    Data(3 * cm, 120 * V, 0.534 * A),
    Data(3 * cm, 140 * V, 0.735 * A),
    Data(3 * cm, 160 * V, 1.730 * A),
    Data(3 * cm, 180 * V, 2.041 * A),
    Data(3 * cm, 200 * V, 2.275 * A),
    Data(3 * cm, 220 * V, 2.409 * A),
    Data(3 * cm, 240 * V, 2.529 * A),
    Data(3 * cm, 260 * V, 2.635 * A),
    Data(3 * cm, 280 * V, 2.767 * A),
    Data(3 * cm, 300 * V, 2.864 * A),

    Data(2 * cm, 120 * V, 1.770 * A),
    Data(2 * cm, 140 * V, 2.670 * A),
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
]


def find_intermediary_point(data: list[tuple[float, float]], x: float) -> float:
    from scipy.interpolate import interp1d

    x_values, y_values = zip(*data)
    interpolation_function = interp1d(x_values, y_values, kind='linear', fill_value='extrapolate')
    y = interpolation_function(x)

    return y


def main():
    table1 = PrettyTable()
    table1.field_names = ["r (cm)", "U", "I_1", "I_2", "I_3", "I_4", "I_5", "I_m", "sigma_I_m", "epsilon_I_m", "B", "e/m"]

    for data in data1:
        table1.add_row([data.r, data.U, data.I_1, data.I_2, data.I_3, data.I_4, data.I_5, data.I_m, data.sigma_I_m, data.epsilon_I_m, data.B, data.e_over_m])
        print(f"{data.B=}")

    e_over_m_median = Median([data.e_over_m for data in data1]).median
    write_to_csv("table1.csv", table1)
    print(f"{e_over_m_median=}")

    table2 = PrettyTable()
    table2.field_names = ["U", "I_r5", "e/m_r5", "I_r4", "e/m_r4", "I_r3", "e/m_r3", "I_r2", "e/m_r2"]

    for i in range(0, 10):
        d0 = data2[i]
        d1 = data2[i + 10]
        d2 = data2[i + 20]
        d3 = data2[i + 30]

        table2.add_row([
            d0.U if d0 is not None else d1.U if d1 is not None else d2.U if d2 is not None else d3.U,
            None if d0 is None else d0.I, None if d0 is None else d0.e_over_m,
            None if d1 is None else d1.I, None if d1 is None else d1.e_over_m,
            None if d2 is None else d2.I, None if d2 is None else d2.e_over_m,
            None if d3 is None else d3.I, None if d3 is None else d3.e_over_m
        ])

    print([data.e_over_m for data in data2 if data is not None])
    median = Median([data.e_over_m for data in data2 if data is not None])
    e_over_m_median = median.median
    sigma_e_over_m = median.square_deviation

    write_to_csv("table2.csv", table2)
    print(f"{e_over_m_median=}")
    print(f"{sigma_e_over_m=}")

    table3 = PrettyTable()


    """
    I 1.70
    U_base 25V
    r 3   3.5 4   4.5 5
    U 157 175 203 252 302
    """
    table3.field_names = ["r (cm)", "3.0", "3.5", "4.0", "4.5", "5.0"]
    table3.add_row(["U (V)", 157, 175, 203, 252, 302])

    write_to_csv("table3.csv", table3)

if __name__ == "__main__":
    delete_file("results.txt")
    main()
