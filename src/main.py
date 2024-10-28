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
                             U_0=[1.262, 1.186, 1.176, 1.144, 1.08, 1.163, 1.093, 1.127, 1.089, 1.102] * V
                         )
                     ]
    )
    run_with_data(all_data, "data_table_all.csv", "data_plot_all.png", "results_all.txt")
    run_with_data(data_no_uv, "data_table_no_uv.csv", "data_plot_no_uv.png", "results_no_uv.txt")

    append_to_file("general_results.txt", "Q: In ce consta efectul fotoelectric?")
    append_to_file("general_results.txt", "A: Efectul foloeletric consta in emiterea de electroni de pe suprafata unui material atunci cand acesta este expus la lumina de o anumita frecventa sau lungime de unda. In acest fenomen, fotonii cu energie sugicienta sunt absorbiti de electronii de pe suprafata materialului, iar acesta sunt eliberati daca energia fotonului este mai mare decat energia necesara pentru a depasii forta de atractie dintre electron si material")
    append_to_file("general_results.txt", "Q: Scrieti ecuatia de conservare a energiei in procesul de ciocnire foron-electron.")
    append_to_file("general_results.txt", "A: E_foton = E_forta + E_cinetica. E_forta este energia minima necesara pentru a elibera electronul de pe suprafata materialului, iar E_cinetica este energia cinetica a electronului eliberat.")
    append_to_file("general_results.txt", "Q: Ce se intelege prin frecventa de prag?")
    append_to_file("general_results.txt", "A: Frecventa de prag este frecventa minima a radiatiei incidenta necesara pentru a produce efectul fotoelectric.")
    append_to_file("general_results.txt", "Q: Ce este constanta lui Planck? Stabiliti unitatea de masura a acesteia.")
    append_to_file("general_results.txt", "A: Constanta lui Planck este o constanta fizica, care exprima proportionalitatea dintre energia unui foton si frecenta acestuia. Unitatea de masura estg J*s (Jouli * secunda) sau eV (electron-volt).")
    append_to_file("general_results.txt", "Q: Enuntati posibilele surse de erori din cadrul experimentului si sugerati metode de reducere a erorilor.")
    append_to_file("general_results.txt", "A: Reflexia si absortila partiala a luminii care poate fi solutionata prin mentirea suprafetei curate. In functie de temperatura care poate fi solutionata prin mentinerea unei temperaturi constante pe parcursul experimentului.")


if __name__ == "__main__":
    main()
