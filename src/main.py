from __future__ import division

from unum.units import *

from constants import CONSTANTS
from table_setup import Data, WaveLength
from utils import write_to_csv, append_to_file

"""
Scopul lucrarii:
- Determinarea constantei de Planck din studiul efectului foloelectric extern.
"""


def run_with_data(data: Data, data_table_file: str, data_plot_file: str, results_file: str):
    write_to_csv(data_table_file, data.create_table())
    h, v_p = data.plot(data_plot_file)
    append_to_file(results_file, f"h = {h * (10 ** 34):.2f}e-34 J*s")
    append_to_file(results_file, f"v_p = {v_p.asUnit(Hz).asNumber() / (10 ** 12):.2f} * 10^12 Hz")
    lambda_p = CONSTANTS.c / v_p
    append_to_file(results_file, f"lambda_p = {lambda_p.asUnit(nm).asNumber():.2f} nm")

    L_extraction = h * v_p
    append_to_file(results_file, f"L_extr = {(L_extraction.asNumber() * J).asUnit(eV).asNumber():.2f} eV")


def main():
    data_no_uv: Data = Data(
        wave_lengths=[
            WaveLength(
                color="galben",
                wave_length=578 * nm,
                U_0=[0.736, 0.875, 0.694, 0.738, 0.738, 0.742, 0.755, 0.715, 0.714, 0.75] * V
            ),
            WaveLength(
                color="verde",
                wave_length=546 * nm,
                U_0=[0.838, 0.865, 0.836, 0.861, 0.857, 0.866, 0.869, 0.865, 0.842, 0.852] * V
            ),
            WaveLength(
                color="albastru",
                wave_length=436 * nm,
                U_0=[1.192, 1.259, 1.204, 1.215, 1.2, 1.206, 1.272, 1.232, 1.2, 1.167] * V
            ),
            WaveLength(
                color="violet",
                wave_length=405 * nm,
                U_0=[1.2, 1.304, 1.273, 1.309, 1.265, 1.301, 1.32, 1.361, 1.288, 1.299] * V
            ),
        ]
    )

    all_data = Data(
        wave_lengths=data_no_uv.wave_lengths[::] +
                     [
                         WaveLength(
                             color="ultraviolet",
                             wave_length=366 * nm,
                             U_0=[1.262, 1.136, 1.076, 1.014, 1.08, 1.063, 1.043, 1.037, 1.089, 1] * V
                         )
                     ]
    )
    run_with_data(all_data, "results_all.txt", "data_table_all.csv", "data_plot_all.png")
    run_with_data(data_no_uv, "results_no_uv.txt", "data_table_no_uv.csv", "data_plot_no_uv.png")


if __name__ == "__main__":
    main()
