import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
from unum import Unum
from unum.units import *

from table_setup import MinimumIntensityData, MaximumIntensityData, MinimumIntensityComputedData, MaximumIntensityComputedData, HeisenbergData
from utils import get_column, write_to_csv, delete_file, append_to_file, kV, mV

RESULTS_FILE: str = "results.txt"
MINIMUM_INTENSITY_TABLE_FILE: str = "minimum_intensity.csv"
MAXIMUM_INTENSITY_TABLE_FILE: str = "maximum_intensity.csv"
MINIMUM_INTENSITY_WAVE_LENGTH_TABLE_FILE: str = "minimum_intensity_wave_length.csv"
MAXIMUM_INTENSITY_WAVE_LENGTH_TABLE_FILE: str = "maximum_intensity_wave_length.csv"
HEISENBERG_TABLE_FILE: str = "heisenberg.csv"

"""
Scopul lucrarii:
- Se masoara distributia intensitatii luminoase difractate prin fante de largimi variabile
- Se masoara lungimea de unda a radiatiei difractate
- Se verifica corespondenta dintre teorie si experiment in ceea ce priveste pozitiile si intensitatile maximelor de intesitate luminoasa 
"""

MINIMUM_INTENSITY_DATA: MinimumIntensityData = MinimumIntensityData(
    left_of_central_minimum_3=[0 * mm, 0 * mm, 0 * mm],  # List of 3 measurements
    left_of_central_minimum_2=[0 * mm, 0 * mm, 0 * mm],  # List of 3 measurements
    left_of_central_minimum_1=[0 * mm, 0 * mm, 0 * mm],  # List of 3 measurements
    right_of_central_minimum_1=[0 * mm, 0 * mm, 0 * mm],  # List of 3 measurements
    right_of_central_minimum_2=[0 * mm, 0 * mm, 0 * mm],  # List of 3 measurements
    right_of_central_minimum_3=[0 * mm, 0 * mm, 0 * mm],  # List of 3 measurements
)

MAXIMUM_INTENSITY_DATA: MaximumIntensityData = MaximumIntensityData(
    left_of_central_maximum_3=MaximumIntensityData.Measurement(
        slot_A=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_B=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_C=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
    ),
    left_of_central_maximum_2=MaximumIntensityData.Measurement(
        slot_A=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_B=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_C=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
    ),
    left_of_central_maximum_1=MaximumIntensityData.Measurement(
        slot_A=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_B=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_C=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
    ),
    central_maximum=MaximumIntensityData.Measurement(
        slot_A=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_B=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_C=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
    ),
    right_of_central_maximum_1=MaximumIntensityData.Measurement(
        slot_A=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_B=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_C=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
    ),
    right_of_central_maximum_2=MaximumIntensityData.Measurement(
        slot_A=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_B=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_C=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
    ),
    right_of_central_maximum_3=MaximumIntensityData.Measurement(
        slot_A=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_B=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
        slot_C=MaximumIntensityData.Measurement.Slot(0 * mm, 0 * mV),
    )
)

HEISENBERG_DATA: HeisenbergData = HeisenbergData(
    slot_A_left=[0 * mm, 0 * mm, 0 * mm, 0 * mm],  # List of 4 measurements
    slot_A_right=[0 * mm, 0 * mm, 0 * mm, 0 * mm],  # List of 4 measurements
    slot_B_left=[0 * mm, 0 * mm, 0 * mm, 0 * mm],  # List of 4 measurements
    slot_B_right=[0 * mm, 0 * mm, 0 * mm, 0 * mm],  # List of 4 measurements
    slot_C_left=[0 * mm, 0 * mm, 0 * mm, 0 * mm],  # List of 4 measurements
    slot_C_right=[0 * mm, 0 * mm, 0 * mm, 0 * mm],  # List of 4 measurements
    lambda_= 0 * nm,
)


def main():
    minimum_intensity_table = MINIMUM_INTENSITY_DATA.create_table()
    write_to_csv(MINIMUM_INTENSITY_TABLE_FILE, minimum_intensity_table)

    maximum_intensity_table = MAXIMUM_INTENSITY_DATA.create_table()
    write_to_csv(MAXIMUM_INTENSITY_TABLE_FILE, maximum_intensity_table)

    computed_minimum_intensity_computed_data: MinimumIntensityComputedData = MinimumIntensityComputedData(MINIMUM_INTENSITY_DATA)
    write_to_csv(MINIMUM_INTENSITY_WAVE_LENGTH_TABLE_FILE, computed_minimum_intensity_computed_data.create_table())
    lambda_ = computed_minimum_intensity_computed_data.get_median().median.asUnit(nm)
    if lambda_ == 0 * nm:
        lambda_ = 0.0001 * nm
    lambda_error = computed_minimum_intensity_computed_data.get_median().square_deviation.asUnit(nm)

    computed_maximum_intensity_computed_data: MaximumIntensityComputedData = MaximumIntensityComputedData(MAXIMUM_INTENSITY_DATA, lambda_)
    write_to_csv(MAXIMUM_INTENSITY_WAVE_LENGTH_TABLE_FILE, computed_maximum_intensity_computed_data.create_table())

    append_to_file(RESULTS_FILE, f"lambda = ({lambda_} +- {lambda_error}) nm")
    append_to_file(RESULTS_FILE, f"Q: Care este diferenta dintre difractie si interferenta? Dar intre difractie si refractie?")
    append_to_file(RESULTS_FILE, f"A: TODO")
    append_to_file(RESULTS_FILE, f"Q: Ce influenta are difractia optica asupra imaginii vazupe pe suprafata unui CD sau DVD pe care cade lumina? Ce se petrece cand inclinam suprafata lor sub unghiuri de incidenta diferite?")
    append_to_file(RESULTS_FILE, f"A: TODO")
    append_to_file(RESULTS_FILE, f"Q: Cum influenteaza fenomenul de difractie, capacitatea unui intrument optic de a distringe doua puncte foarte apropiate dintr-o imagine?")
    append_to_file(RESULTS_FILE, f"A: TODO")
    append_to_file(RESULTS_FILE, f"Q: Lumina unui laser este proiectate pe un ecran circular de diamentru d. Cum influeneata difractia marimea imaginii obtinute pe un ecran aflat la o distanta oarecare de ecran?")
    append_to_file(RESULTS_FILE, f"A: TODO")
    append_to_file(RESULTS_FILE, f"Q: Ce se petrece cu imaginea de pe ecranul din fig.1.b, daca diamentru fasciculului laser, incident in centru fantei, este mai mic decat latimea fantei; dat daca este mai mare?")
    append_to_file(RESULTS_FILE, f"A: TODO")

    HEISENBERG_DATA.compute(lambda_)
    write_to_csv(HEISENBERG_TABLE_FILE, HEISENBERG_DATA.create_table())

    append_to_file(RESULTS_FILE, f"Q: Este posibil, conform relatiei dE * dT >= h, ca daca obtinem intr-un experiment ca dt sa tinda spre zero, sa obtinem energie? Daca da, de unde? Este incalcat cumva principiul convervarii energiei?")
    append_to_file(RESULTS_FILE, f"A: TODO")
    append_to_file(RESULTS_FILE, f"Q: Un flux de particule trece prin fanta din fig.1 si cade pe un ecran E aflat la o distranta oarecare de fanta. Este oare posibil sa obtinem pe ecran, (prin ingustarea fantei), o pata de particule oricat de mica? Oferiti o explicatie in termenii relatiilor de nedeterminare ale lui Heisenberg.")
    append_to_file(RESULTS_FILE, f"A: TODO")
    append_to_file(RESULTS_FILE, f"Q: Ce aplicatii tehnice vedeti pentru relatiile 2a si dE * dt >= h?")
    append_to_file(RESULTS_FILE, f"A: TODO")
    append_to_file(RESULTS_FILE, f"Q: Ce expliucatii gasiti daca paramentru k_H se dovedeste a fi neunitar?")
    append_to_file(RESULTS_FILE, f"A: TODO")


if __name__ == "__main__":
    delete_file(RESULTS_FILE)
    delete_file(MINIMUM_INTENSITY_TABLE_FILE)
    main()
