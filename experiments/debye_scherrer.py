import random

from prettytable import PrettyTable
from unum.units import *
from unum import Unum
import matplotlib.pyplot as plot

from utils import get_column, get_columns, strip_measurement_units, get_median_and_error

kV = Unum.unit('kV', 1000 * V)  # 1 kV = 1000 V

"""
Scopul lucrarii:
- Determinarea lungimii de unda asociata electronilor
- Verificarea ecuatiei de Broglie
- Determinarea constantelor de retea ale grafitului
"""

# Constants
CONST_d1 = 2.13 * 10 ** -10 * m
CONST_d2 = 1.23 * 10 ** -10 * m
CONST_L = 13.5 * cm

CONST_e = 1.602 * 10 ** -19 * C
CONST_m = 9.109 * 10 ** -31 * kg
CONST_h = 6.625 * 10 ** -34 * J * s

# Experimental data
experimental_data = [
    {
        "U": 3 * kV,
        "D1": 0 * cm,
        "D2": 0 * cm,
    },
    {
        "U": 3.5 * kV,
        "D1": 0 * cm,
        "D2": 0 * cm,
    },
    {
        "U": 4 * kV,
        "D1": 0 * cm,
        "D2": 0 * cm,
    },
    {
        "U": 4.5 * kV,
        "D1": 0 * cm,
        "D2": 0 * cm,
    },
    {
        "U": 5 * kV,
        "D1": 0 * cm,
        "D2": 0 * cm,
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


def compute_graphite_constants(D: Unum, U_inverse_square_root: Unum) -> Unum:
    divided = 2 * CONST_h * CONST_L
    divider = D * (2 * CONST_m * CONST_e) ** (1 / 2)
    return (U_inverse_square_root * divided / divider).asNumber() * m


def main():
    table = PrettyTable()

    number = 5

    for data in experimental_data:
        if data["D1"] == 0 * cm:
            data["D1"] = number * cm
        if data["D2"] == 0 * cm:
            data["D2"] = (number + 1) * cm
        number -= 1

    table.add_column("U (kV)", [entry["U"].asUnit(kV) for entry in experimental_data])
    table.add_column("1/U^1/2 (V^-1/2)", [computer_inverse_square_root(entry["U"]).asUnit(1 / V ** 0.5) for entry in experimental_data])
    table.add_column("D1 (cm)", [entry["D1"].asUnit(cm) for entry in experimental_data])
    table.add_column("D2 (cm)", [entry["D2"].asUnit(cm) for entry in experimental_data])

    table.add_column("λ1 exp (pm)", [compute_wave_length(D1, CONST_d1).asUnit(pm) for D1 in get_column(table, "D1 (cm)")])
    table.add_column("λ2 exp (pm)", [compute_wave_length(D2, CONST_d2).asUnit(pm) for D2 in get_column(table, "D2 (cm)")])

    table.add_column("λ teo (pm)", [compute_theoretical_wave_length(data).asUnit(pm) for data in get_column(table, "1/U^1/2 (V^-1/2)")])

    print(get_columns(table, ["D1 (cm)", "1/U^1/2 (V^-1/2)"]))

    table.add_column("d1 exp (pm)", [compute_graphite_constants(
        entries[0], # maybe cast to meters
        entries[1]
    ) for entries in get_columns(table, ["D1 (cm)", "1/U^1/2 (V^-1/2)"])
    ])

    table.add_column("d2 exp (pm)", [compute_graphite_constants(
        entries[0], # maybe cast to meters
        entries[1]
    ) for entries in get_columns(table, ["D2 (cm)", "1/U^1/2 (V^-1/2)"])
    ])


    D1_entries = [entry.asNumber() for entry in get_column(table, "D1 (cm)")]
    D2_entries = [entry.asNumber() for entry in get_column(table, "D2 (cm)")]
    U_entries = [entry.asNumber() for entry in get_column(table, "1/U^1/2 (V^-1/2)")]

    plot.plot(U_entries, D1_entries)
    plot.plot(U_entries, D2_entries)
    plot.ylabel("D1 and D2 in cm")

    plot.xlabel("1/U^1/2 in V")


    d1_exp_median, d1_exp_error_median = get_median_and_error(get_column(table, "d1 exp (pm)"))
    d2_exp_median, d2_exp_error_median = get_median_and_error(get_column(table, "d2 exp (pm)"))

    print(strip_measurement_units(table))
    print(f"d1 exp = {d1_exp_median.asUnit(pm)} +- {d1_exp_error_median.asUnit(pm)}")
    print(f"d2 exp = {d2_exp_median.asUnit(pm)} +- {d2_exp_error_median.asUnit(pm)}")

    plot.show()
