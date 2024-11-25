import numpy as np
from prettytable import PrettyTable

from utils import write_to_csv
from utils import delete_file
import matplotlib.pyplot as plt


class Specter:
    color_name: str
    wavelength: float
    x: float

    def __init__(self, color_name: str, wavelength: float, x_degree: float, x_minutes: float):
        self.color_name = color_name
        self.wavelength = wavelength
        self.x = x_degree + x_minutes / 60


helium_specter: list[Specter] = [
    Specter("rosu", 504.774, 115, 50),
    Specter("portocaliu", 501.567, 116, 2),
    Specter("galben", 492.193, 116, 36),
    Specter("turcuaz", 471.314, 117, 5),
    Specter("albsatru slab", 447.148, 117, 6),
    Specter("albastru intens", 443.755, 118, 0),
    Specter("violet", 438.793, 118, 25)
]

unkown_specter: list[Specter] = [
    Specter("rosu slab 2", 0, 116, 12),
    Specter("rosu intens", 0, 116, 17),
    Specter("rosu slab 1", 0, 116, 22),
    Specter("portocaliu", 0, 116, 30),
    Specter("portocaliu slab", 0, 116, 30 + 6),
    Specter("galben", 0, 116, 30 + 9),
    Specter("turcuaz", 0, 117, 10), # - 5
    Specter("albastru", 0, 117, 30 + 10),
    Specter("violet", 0, 118, 30 + 22)
]

def main():
    helium_specter_table = PrettyTable()
    unknown_specter_table = PrettyTable()

    helium_specter_table.field_names = ["Color Name", "Wavelength", "X"]
    unknown_specter_table.field_names = ["Color Name", "Wavelength", "X"]

    for specter in helium_specter:
        helium_specter_table.add_row([specter.color_name, specter.wavelength, specter.x])


    x = [specter.x for specter in helium_specter]
    y = [1 / (specter.wavelength ** 2) for specter in helium_specter]

    a, b = np.polyfit(x, y, 1)
    plt.plot(x, y, "o")
    plt.plot(x, [a * x_value + b for x_value in x])
    plt.xlabel("x")
    plt.ylabel("1/lambda^2")
    plt.show()

    for specter in unkown_specter:
        wave_length = 1 / (a * specter.x + b)
        wave_length = wave_length ** (1 / 2)
        unknown_specter_table.add_row([specter.color_name, wave_length, specter.x])

    write_to_csv("helium_specter_table.csv", helium_specter_table)
    write_to_csv("unknown_specter_table.csv", unknown_specter_table)

if __name__ == "__main__":
    delete_file("results.txt")
    main()
