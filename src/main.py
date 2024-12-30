from cmath import e, pi
from prettytable import PrettyTable
from unum import Unum
from unum.units import s, min, A, T, eV, cm, V, N, m

from utils import Median
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

    def __init__(self, r: Unum, U: Unum, I: list[Unum]):
        self.r = r
        self.U = U
        self.I = Median(I).median
        term_1 = (125 / 32)
        term_2_1 = R ** 2
        term_2_2 = miu_0 ** 2 * n ** 2
        term_2 = term_2_1 / term_2_2
        term_3 = (U / (r ** 2 * self.I ** 2))
        self.e_over_m = term_1 * term_2 * term_3


data2: list[Data] = [
    Data(5 * cm, 120 * V, [1.02, ] * A),
    Data(5 * cm, 140 * V, [1.16, ] * A),
    Data(5 * cm, 160 * V, [1.27, 1.143333, ] * A),
    Data(5 * cm, 180 * V, [1.238, 1.34, 1.264667, ] * A),
    Data(5 * cm, 200 * V, [1.328, 1.43, 1.438, 1.356333, ] * A),
    Data(5 * cm, 220 * V, [1.398, 1.51, 1.514, 1.422, 1.425, 1.42, ] * A),
    Data(5 * cm, 240 * V, [1.470, 1.57, 1.581, 1.493, 1.481, 1.518, ] * A),
    Data(5 * cm, 260 * V, [1.528, 1.64, 1.652, 1.566, 1.569, 1.577, ] * A),
    Data(5 * cm, 280 * V, [1.627, 1.71, 1.713, 1.627667, 1.647, 1.636, ] * A),
    Data(5 * cm, 300 * V, [1.685, 1.76, 1.77, 1.678667, 1.702, ] * A),

    Data(4 * cm, 120 * V, [0.135, 1.16, 0.133667, ] * A),
    Data(4 * cm, 140 * V, [0.162, 1.26, 0.161667, ] * A),
    Data(4 * cm, 160 * V, [0.192, 1.58, 1.425, ] * A),
    Data(4 * cm, 180 * V, [1.503, 1.68, 1.559667, ] * A),
    Data(4 * cm, 200 * V, [1.673, 1.8, 1.794, 1.687333, 1.788, 1.82, ] * A),
    Data(4 * cm, 220 * V, [1.764, 1.87, 1.858, 1.784333, 1.859, 1.911, ] * A),
    Data(4 * cm, 240 * V, [1.854, 1.95, 2.0, 1.877333, 1.921, 2.001, ] * A),
    Data(4 * cm, 260 * V, [1.937, 2.05, 2.065, 1.957667, 2.066, 2.046, ] * A),
    Data(4 * cm, 280 * V, [1.975, 2.15, 2.1, 2.052, 2.096, ] * A),
    Data(4 * cm, 300 * V, [2.118, 2.24, 2.225, 2.118338, 2.229, ] * A),

    Data(3 * cm, 120 * V, [0.534, 1.81, 0.557667, ] * A),
    Data(3 * cm, 140 * V, [0.735, 1.94, 0.820333, ] * A),
    Data(3 * cm, 160 * V, [1.730, 2.13, 1.852333, ] * A),
    Data(3 * cm, 180 * V, [2.041, 2.29, 2.143333, ] * A),
    Data(3 * cm, 200 * V, [2.275, 2.43, 2.45, 2.284667, 2.419, 2.49, ] * A),
    Data(3 * cm, 220 * V, [2.409, 2.66, 2.56, 2.408333, 2.55, 2.597, ] * A),
    Data(3 * cm, 240 * V, [2.529, 2.77, 2.69, 2.517667, 2.666, 2.682, ] * A),
    Data(3 * cm, 260 * V, [2.635, 2.84, 2.815, 2.643667, 2.785, 2.685, ] * A),
    Data(3 * cm, 280 * V, [2.767, 2.93, 2.9, 2.797667, 2.897, ] * A),
    Data(3 * cm, 300 * V, [2.864, 3.03, 2.931, 2.844667, 3.005, ] * A),

    Data(2 * cm, 120 * V, [1.770, 2.86, 1.92167, ] * A),
    Data(2 * cm, 140 * V, [2.670, 2.887333, ] * A),
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
