import numpy as np
from matplotlib import pyplot as plt
from prettytable import PrettyTable
from unum import Unum
from unum.units import *

from constants import CONSTANTS, Constants
from utils import Median


class WaveLength:
    color: str
    wave_length: Unum
    U_0: list[Unum]  # List of 10 measurements
    U_0_median: Unum
    v: Unum

    def __init__(self, color: str, wave_length: Unum, U_0: list[Unum]):
        self.color = color
        self.wave_length = wave_length
        self.U_0 = U_0
        self.U_0_median = Median(data=U_0).median
        self.v = CONSTANTS.c / wave_length


class Data:
    wave_lengths: list[WaveLength]

    def __init__(self, wave_lengths: list[WaveLength]):
        self.wave_lengths = wave_lengths

    def create_table(self):
        table = PrettyTable()

        table.add_column(
            "Filtru",
            [wave_length.color for wave_length in self.wave_lengths]
        )

        table.add_column(
            "lambda (mm)",
            [wave_length.wave_length for wave_length in self.wave_lengths]
        )

        for index in range(10):
            column = []

            for wave_length in self.wave_lengths:
                column += [wave_length.U_0[index].asUnit(V)]
            table.add_column(f"U0_{str(index + 1)} (V)", column)

        table.add_column(
            "U_0 median (V)",
            [wave_length.U_0_median.asUnit(V) for wave_length in self.wave_lengths]
        )

        table.add_column(
            "v * 10^12 median (V)",
            [(wave_length.v/10**12).asUnit(Hz) for wave_length in self.wave_lengths]
        )

        return table

    def plot(self, file_name:str):
        x = [(wave_length.v.asUnit(Hz).asNumber())/10**12 for wave_length in self.wave_lengths]
        y = [wave_length.U_0_median.asUnit(V).asNumber() for wave_length in self.wave_lengths]

        slope, intercept = np.polyfit(x, y, 1)
        pred = slope * np.array(x) + intercept
        plt.plot(x, pred, color="red", label=f"Linear Fit: y = {slope:.2f}x + {intercept:.2f}")

        plt.scatter(x, y)
        plt.xlabel("v * 10^12 (Hz)")

        plt.show()
        plt.savefig(file_name)
