from __future__ import division

from unum.units import *

from constants import CONSTANTS
from table_setup import Data, WaveLength
from utils import write_to_csv, delete_file, append_to_file

RESULTS_FILE: str = "results.txt"
DATA_TABLE_FILE: str = "data_table.csv"
DATA_PLOT_FILE: str = "data_plot.png"

"""
Scopul lucrarii:
- Determinarea constantei de Planck din studiul efectului foloelectric extern.
"""

DATA: Data = Data(
    wave_lengths=[
        WaveLength(
            color="galben",
            wave_length=578 * nm,
            # U_0=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * V
            U_0=[1 for _ in range(10)] * V
        ),
        WaveLength(
            color="verde",
            wave_length=546 * nm,
            # U_0=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * V
            U_0=[4 for _ in range(10)] * V
        ),
        WaveLength(
            color="albastru",
            wave_length=436 * nm,
            # U_0=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * V
            U_0=[8 for _ in range(10)] * V
        ),
        WaveLength(
            color="violet",
            wave_length=405 * nm,
            # U_0=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * V
            U_0=[3 for _ in range(10)] * V
        ),
        WaveLength(
            color="ultraviolet",
            wave_length=366 * nm,
            # U_0=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * V
            U_0=[10 for _ in range(10)] * V
        )
    ]
)


def main():
    write_to_csv(DATA_TABLE_FILE, DATA.create_table())
    h, v_p = DATA.plot(DATA_PLOT_FILE)
    append_to_file(RESULTS_FILE, f"h = {h * (10 ** 33):.2f}e-33 J*s")
    append_to_file(RESULTS_FILE, f"v_p = {v_p.asUnit(Hz).asNumber() / (10 ** 12):.2f} * 10^12 Hz")
    lambda_p = CONSTANTS.c / v_p
    append_to_file(RESULTS_FILE, f"lambda_p = {lambda_p.asUnit(nm).asNumber()} nm")

    L_extrema = h * v_p
    append_to_file(RESULTS_FILE, f"L_extr = {L_extrema.asNumber() * 10 ** 18:.2f}e-18 J")


if __name__ == "__main__":
    delete_file(RESULTS_FILE)
    delete_file(DATA_TABLE_FILE)
    main()
