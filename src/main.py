import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
from unum import Unum
from unum.units import *

from utils import get_column, write_to_csv, delete_file, append_to_file, kV

RESULTS_FILE: str = "../results.txt"
TABLE_FILE: str = "../table.csv"

"""
Scopul lucrarii:
- Determinarea lungimii de unda asociata electronilor
- Verificarea ecuatiei de Broglie
- Determinarea constantelor de retea ale grafitului
"""

# Constants
CONST_d1 = 2.13 * 10 ** -10 * m
CONST_d2 = 1.23 * 10 ** -10 * m
CONST_L = (13.5 * cm).asUnit(m)

CONST_e = 1.602 * 10 ** -19 * C
CONST_m = 9.109 * 10 ** -31 * kg
CONST_h = 6.625 * 10 ** -34 * J * s

# Experimental data
experimental_data = [
    {
        "U": 3 * kV,
        "D1": 2.85 * cm,
        "D2": 4.85 * cm,
    },
    {
        "U": 3.5 * kV,
        "D1": 2.75 * cm,
        "D2": 4.7 * cm,
    },
    {
        "U": 4 * kV,
        "D1": 2.55 * cm,
        "D2": 4.2 * cm,
    },
    {
        "U": 4.5 * kV,
        "D1": 2.4 * cm,
        "D2": 4 * cm,
    },
    {
        "U": 5 * kV,
        "D1": 2.25 * cm,
        "D2": 3.9 * cm,
    }
]


def compute_wave_length(D: Unum, d: Unum) -> Unum:
    return d * D / (2 * CONST_L)


def computer_inverse_square_root(U: Unum) -> Unum:
    divider = U ** (1 / 2)
    return 1 / divider


def compute_theoretical_wave_length(U_inverse_square_root: Unum) -> Unum:
    divider = ((2 * CONST_m * CONST_e) ** (1 / 2))
    return (U_inverse_square_root * CONST_h / divider).asNumber() * m


def compute_graphite_constants(slope: float) -> Unum:
    divided = 2 * CONST_h * CONST_L
    divider = (2 * CONST_m * CONST_e) ** (1 / 2) * slope

    return (divided / divider).asNumber() * m


def main():

    table: PrettyTable = PrettyTable()

    table.add_column("U (kV)", [entry["U"].asUnit(kV) for entry in experimental_data])
    table.add_column("1/U^1/2 (V^-1/2)", [computer_inverse_square_root(entry["U"]).asUnit(1 / V ** 0.5) for entry in experimental_data])
    table.add_column("D1 (cm)", [entry["D1"].asUnit(cm) for entry in experimental_data])
    table.add_column("D2 (cm)", [entry["D2"].asUnit(cm) for entry in experimental_data])

    table.add_column("λ1 exp (pm)", [compute_wave_length(D1, CONST_d1).asUnit(pm) for D1 in get_column(table, "D1 (cm)")])
    table.add_column("λ2 exp (pm)", [compute_wave_length(D2, CONST_d2).asUnit(pm) for D2 in get_column(table, "D2 (cm)")])

    table.add_column("λ teo (pm)", [compute_theoretical_wave_length(data).asUnit(pm) for data in get_column(table, "1/U^1/2 (V^-1/2)")])

    U_entries: list[float] = [entry.asNumber() for entry in get_column(table, "1/U^1/2 (V^-1/2)")]

    D1_entries: list[float] = [entry.asUnit(m).asNumber() for entry in get_column(table, "D1 (cm)")]
    D2_entries: list[float] = [entry.asUnit(m).asNumber() for entry in get_column(table, "D2 (cm)")]

    plt.scatter(U_entries, D1_entries)
    plt.scatter(U_entries, D2_entries)
    plt.ylabel("D1 and D2 in cm")
    plt.xlabel("1/U^1/2 in 1/V^-1/2")

    D1_slope, D1_intercept = np.polyfit(U_entries, D1_entries, 1)
    D2_slope, D2_intercept = np.polyfit(U_entries, D2_entries, 1)

    D1_pred = D1_slope * np.array(U_entries) + D1_intercept
    plt.plot(U_entries, D1_pred, color="red", label=f"Linear Fit: y = {D1_slope:.2f}x + {D1_intercept:.2f}")

    D2_pred = D2_slope * np.array(U_entries) + D2_intercept
    plt.plot(U_entries, D2_pred, color="red", label=f"Linear Fit: y = {D2_slope:.2f}x + {D2_intercept:.2f}")

    d1_exp = compute_graphite_constants(D1_slope)
    d2_exp = compute_graphite_constants(D2_slope)

    append_to_file(RESULTS_FILE, f"d1 exp = {d1_exp.asUnit(m).asNumber()*(10**10):.2f}e-10 m")
    append_to_file(RESULTS_FILE, f"d2 exp = {d2_exp.asUnit(m).asNumber()*(10**10):.2f}e-10 m")

    write_to_csv(TABLE_FILE, table)
    plt.show()
    plt.savefig("../plot.png")


if __name__ == "__main__":
    delete_file(RESULTS_FILE)
    delete_file(TABLE_FILE)
    main()
