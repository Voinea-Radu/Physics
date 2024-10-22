from __future__ import division

import builtins

import matplotlib.pyplot as plt
import numpy as np
from numpy.ma.core import minimum
from prettytable import PrettyTable
from scipy.optimize import fsolve
from unum import Unum
from unum.units import *
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

from constants import CONSTANTS
from table_setup import Data, WaveLength
from utils import get_column, write_to_csv, delete_file, append_to_file, kV, mV, Median

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
            U_0=[10 for _ in range(10)] * V
        ),
        WaveLength(
            color="verde",
            wave_length=546 * nm,
            # U_0=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * V
            U_0=[8 for _ in range(10)] * V
        ),
        WaveLength(
            color="albastru",
            wave_length=436 * nm,
            # U_0=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * V
            U_0=[4 for _ in range(10)] * V
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
            U_0=[1 for _ in range(10)] * V
        )
    ]
)


def main():
    write_to_csv(DATA_TABLE_FILE, DATA.create_table())
    DATA.plot(DATA_PLOT_FILE)


if __name__ == "__main__":
    delete_file(RESULTS_FILE)
    delete_file(DATA_TABLE_FILE)
    main()
