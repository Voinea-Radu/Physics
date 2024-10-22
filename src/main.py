from __future__ import division

import builtins

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from unum import Unum
from unum.units import mm, nm

from constants import CONSTANTS
from table_setup import MinimumIntensityData, MaximumIntensityData, MinimumIntensityComputedData, MaximumIntensityComputedData, HeisenbergData, Slot
from utils import write_to_csv, delete_file, append_to_file, mV, Median

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


def plot(slot: str, y) -> Slot:
    offset = y.index(max(y))
    x = [entry - offset for entry in list(range(len(y)))]

    x_smooth = np.linspace(builtins.min(x), max(x), 300)
    spline = make_interp_spline(x, y)
    y_smooth = spline(x_smooth)

    central_max_index = np.argmax(y_smooth)

    x_smooth_left = x_smooth[:central_max_index]
    y_smooth_left = y_smooth[:central_max_index]
    x_smooth_right = x_smooth[central_max_index:]
    y_smooth_right = y_smooth[central_max_index:]

    left_minimums: list[(float, float)] = []
    right_minimums: list[(float, float)] = []
    left_maximums: list[(float, float)] = []
    right_maximums: list[(float, float)] = []

    for index in range(1, len(y_smooth_left) - 1):
        if y_smooth_left[index - 1] > y_smooth_left[index] and y_smooth_left[index] < y_smooth_left[index + 1]:
            left_minimums.append((x_smooth_left[index], y_smooth_left[index]))

    for index in range(1, len(y_smooth_left) - 1):
        if y_smooth_left[index - 1] < y_smooth_left[index] and y_smooth_left[index] > y_smooth_left[index + 1]:
            left_maximums.append((x_smooth_left[index], y_smooth_left[index]))

    for index in range(1, len(y_smooth_right) - 1):
        if y_smooth_right[index - 1] > y_smooth_right[index] and y_smooth_right[index] < y_smooth_right[index + 1]:
            right_minimums.append((x_smooth_right[index], y_smooth_right[index]))

    for index in range(1, len(y_smooth_right) - 1):
        if y_smooth_right[index - 1] < y_smooth_right[index] and y_smooth_right[index] > y_smooth_right[index + 1]:
            right_maximums.append((x_smooth_right[index], y_smooth_right[index]))

    left_minimums: list[Slot.Measurement] = [Slot.Measurement(float(number_tuple[0]) * mm, float(number_tuple[1]) * mV) for number_tuple in left_minimums]
    left_maximums: list[Slot.Measurement] = [Slot.Measurement(float(number_tuple[0]) * mm, float(number_tuple[1]) * mV) for number_tuple in left_maximums]
    right_minimums: list[Slot.Measurement] = [Slot.Measurement(float(number_tuple[0]) * mm, float(number_tuple[1]) * mV) for number_tuple in right_minimums]
    right_maximums: list[Slot.Measurement] = [Slot.Measurement(float(number_tuple[0]) * mm, float(number_tuple[1]) * mV) for number_tuple in right_maximums]

    left_minimums.reverse()
    left_minimums = left_minimums[:3]
    left_minimums.reverse()

    left_maximums = left_maximums[:3]
    left_maximums.reverse()

    right_minimums = right_minimums[:3]
    right_maximums = right_maximums[:3]

    plt.plot(x_smooth, y_smooth, label="Spline Curve")
    plt.scatter(x, y, color="red", label="Original Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.title(f"Slot {slot}")

    plt.show()
    plt.savefig(f"slot_{slot}.png")

    return Slot(
        left_minimums=left_minimums,
        right_minimums=right_minimums,
        left_maximums=left_maximums,
        right_maximums=right_maximums,
        central_maximum=Slot.Measurement(x_smooth[central_max_index] * mm, y_smooth[central_max_index] * mV),
    )


def slot_a() -> Slot:
    y = [0.20, 0.21, 0.19, 0.17, 0.17, 0.20, 0.25, 0.31, 0.34, 0.32, 0.28, 0.26, 0.31, 0.40, 0.53, 0.60, 0.62, 0.58, 0.71, 1.36, 2.7, 5.7, 8.60, 11.9, 13.9, 15.5, 16.4, 12.6, 11.8, 9, 4.9, 3.6, 2.3, 1.4, 1.1, 1, 1.02, 0.81, 0.58, 0.4, 0.31, 0.32, 0.39, 0.41, 0.38, 0.33, 0.24, 0.18, 0.17, 0.19, 0.22, 0.24, 0.23]
    return plot("A", y)


def slot_b() -> Slot:
    y = [0.19, 0.31, 0.28, 0.40, 0.56, 0.41, 0.25, 0.59, 1.35, 1.06, 0.92, 1.55, 1.9, 2.5, 7.5, 35.3, 49.5, 53.7, 41.9, 22.3, 6.7, 4.1, 3.8, 2.4, 1.2, 1.5, 1.2, 0.44, 0.36, 0.73, 0.63, 0.32, 0.38, 0.42, ]
    return plot("B", y)


def lab_c() -> Slot:
    y = [0.7, 1.2, 1.9, 1.8, 1.9, 1.7, 4, 5.5, 8.5, 44.2, 120, 64, 10.5, 7.2, 4.4, 2.9, 1.3, 2.4, 1.1]
    return plot("C", y)


def main():
    A = slot_a()
    B = slot_b()
    # C = lab_c()
    C = None

    minimum_intensity_data = MinimumIntensityData(A)
    minimum_intensity_table = minimum_intensity_data.create_table()
    write_to_csv(MINIMUM_INTENSITY_TABLE_FILE, minimum_intensity_table)

    maximum_intensity_data: MaximumIntensityData = MaximumIntensityData(
        slot_A=A,
        slot_B=B,
    )
    maximum_intensity_table = maximum_intensity_data.create_table()
    write_to_csv(MAXIMUM_INTENSITY_TABLE_FILE, maximum_intensity_table)

    computed_minimum_intensity_computed_data: MinimumIntensityComputedData = MinimumIntensityComputedData(minimum_intensity_data, CONSTANTS.SLOT_A)
    write_to_csv(MINIMUM_INTENSITY_WAVE_LENGTH_TABLE_FILE, computed_minimum_intensity_computed_data.create_table())
    lambda_ = computed_minimum_intensity_computed_data.get_median().median.asUnit(nm)
    lambda_error = computed_minimum_intensity_computed_data.get_median().square_deviation.asUnit(nm)

    computed_maximum_intensity_computed_data: MaximumIntensityComputedData = MaximumIntensityComputedData(
        lambda_=lambda_,
        slot_A=A,
        slot_B=B
    )
    write_to_csv(MAXIMUM_INTENSITY_WAVE_LENGTH_TABLE_FILE, computed_maximum_intensity_computed_data.create_table())

    heisenberg_data = HeisenbergData(
        lambda_=lambda_,
        slot_A_left=[-8, -9, -10, -8.5] * mm,
        slot_A_right=[8.5, 10.5, 8, 9.5] * mm,
        slot_B_left=[-4, -3.5, -4.5, -3] * mm,
        slot_B_right=[4.5, 4, 3.5, 4] * mm,
    )

    K_H_median = Median(heisenberg_data.slot_A.k_H + heisenberg_data.slot_B.k_H + (heisenberg_data.slot_C.k_H if C is not None else []))
    K_H = K_H_median.median
    K_H_error = K_H_median.square_deviation

    write_to_csv(HEISENBERG_TABLE_FILE, heisenberg_data.create_table())

    append_to_file(RESULTS_FILE, f"lambda = ({lambda_.asNumber()} +- {lambda_error.asNumber()}) nm")
    append_to_file(RESULTS_FILE, f"K_H = ({K_H.asNumber()} +- {K_H_error.asNumber()})")
    append_to_file(RESULTS_FILE, f"")
    append_to_file(RESULTS_FILE, f"")
    append_to_file(RESULTS_FILE, f"Q: Care este diferenta dintre difractie si interferenta? Dar intre difractie si refractie?")
    append_to_file(RESULTS_FILE, """A: Difractia si interferenta sunt fenomene optice legate de comportamentul undelor luminoase. 
    Difractia apare atunci cand undele luminoase intalnesc un obstacol sau o fanta si se curbeaza in jurul acestuia, 
    ducand la raspandirea undelor in spatele obstacolului. Interferenta se refera la fenomenul de suprapunere a doua
    sau mai mult unde, rezultand zone de intensitate maxima si minima. Difractia este un proces in care undele sunt
    imprastiate iar interferenta este rezultatul suprapunerii acestor unde. Difractia si reflectia sunt fenomene diferite
    Difractia implica curgerea si imprastierea undelor in jurul unui obstacol, in timp ce reflectia este procesul prin
    care lumina isi schimba directia atunci cand trece dintr-un mediu in altul, datorita schimbarii vitezei sale.
    """)
    append_to_file(RESULTS_FILE, f"""Q: Ce influenta are difractia optica asupra imaginii vazute pe suprafata unui CD sau DVD pe care cade lumina? 
    Ce se petrece cand inclinam suprafata lor sub unghiuri de incidenta diferite?""")
    append_to_file(RESULTS_FILE, f"""A: Difractia joaca un rol important in formarea modelelor de culoare pe suprafata CD-urilor si a DVD-urilor.
    Aceste discuri au microstructuri dispuse circular, care actioneaza ca o grila de difractie. Cand lumina cade pe ele,
    se imprastie si creeaza un spectru de culori vizibile. Atunci cand inclinam discul sub diferite unghiuri, schimbam 
    unghiul de incidenta al luminii, si implicit, unghiul la care sunt difractate diferitele lungimi de unda, 
    ceea ce schimba culorile si intensitatea acestora pe care le vedem pe disc""")
    append_to_file(RESULTS_FILE, f"""Q: Cum influenteaza fenomenul de difractie, capacitatea unui intrument optic de a distinge doua puncte foarte
    apropiate dintr-o imagine?""")
    append_to_file(RESULTS_FILE, f"""A: Difractia limiteaza rezolutia unui intrument optic. Atunci cand lumina trece printr-o lentila sau o deschidere. 
    Daca doua puncte sunt foarte apropiate, modelele de difractie produse de acestea se suprapun, facand dificila 
    distingerea clara a celor doua puncte. Capacitatea unui intrument optic de a rezolva doua puncte apropiate este 
    limitata de lungimea de unda a luminii si dimensiunea deschiderii
    """)
    append_to_file(RESULTS_FILE, f"""Q: Lumina unui laser este proiectata pe un ecran circular de diamentru d. Cum influenteaza difractia marimea
    imaginii obtinute pe un ecran aflat la o distanta oarecare de ecran?""")
    append_to_file(RESULTS_FILE, f"""A: Difractia cauzeaza o extindere a fasciculului laser atunci cand aceasta trece printr-o deschidere limitata. 
    In loc sa obtinem un punct luminos clar pe ecranul de proiectie, vedem un model de difractie format dintr-un 
    disc central luminos si inele concentrice mai slabe. Dimensiunea imaginii depinde de dimensiunea deschiderii 
    si de lungimea de unda a luminii laserului, cu cat deschiderea este mai mica, cu atat modelul de difractie este mai larg.
    """)
    append_to_file(RESULTS_FILE, f"""Q: Ce se petrece cu imaginea de pe ecranul din fig.1.b, daca diamentru fasciculului laser, incident in centru
    fantei, este mai mic decat latimea fantei; dat daca este mai mare?""")
    append_to_file(RESULTS_FILE, f"""A: Daca diametrul fascilulului laser este mai mic decat latimea fantei, lumina va trece aproape neperturbata, 
    iar modelul de difractie va fi mai restrans. Daca diametrul fasciculului laser este mai mare decat latimea 
    fantei, lumina va fi difractata mai intens si modelul de difractie va devenii mai larg. Astfel, marimea 
    fasciculului in raport cu fanta influenteaza cat de mult se raspandeste lumina pe ecran.
    """)
    append_to_file(RESULTS_FILE, f"""Q: Este posibil, conform relatiei dE * dT >= h, ca daca obtinem intr-un experiment ca dt sa tinda spre zero, 
    sa obtinem energie? Daca da, de unde? Este incalcat cumva principiul conservarii energiei?""")
    append_to_file(RESULTS_FILE, f"""A: Daca dt tinde spre zero, dE devine foarte mare, dar acest lucru nu inseamna ca energia poate fi creata din 
    nimic, ci ca exista fluctuatii energetice pe perioade foarte scurte de timp. Aceste fluctuatii sunt posibile 
    conform principiilor mecanicii cuantice si nu incalca principiul conservarii energiei deoarece energia medie 
    pe termen lung este constanta.
    """)
    append_to_file(RESULTS_FILE, f"""Q: Un flux de particule trece prin fanta din fig.1 si cade pe un ecran E aflat la o distanta oarecare de fanta. 
    Este oare posibil sa obtinem pe ecran, (prin ingustarea fantei), o pata de particule oricat de mica? 
    Oferiti o explicatie in termenii relatiilor de nedeterminare ale lui Heisenberg.""")
    append_to_file(RESULTS_FILE, f"""A: Nu, nu este posibil sa obtinem o pata de particule oricat de mica, prin ingustarea fantei. Conform 
    principiului incertitudinii lui Heisenberg, daca ingustam fanta, determinam mai precis pozitia 
    particulelor, dar crestem incertitudinea impulsului lor. Aceasta crestere a incertitudinii impulsului 
    determina o raspandire mai mare a particulelor dupa trecerea prin fanta, ceea ce duce la o extindere a 
    pantei pe ecran. Acest efect este rezultatul direct al principiului incertitudinii, care sugereaza ca 
    nu putem masura simultan pozitia si impulsul cu precizie infinita.
    """)
    append_to_file(RESULTS_FILE, f"""Q: Ce aplicatii tehnice vedeti pentru relatiile 2a si dE * dt >= h?""")
    append_to_file(RESULTS_FILE, f"""A: Relatiile de incertitudine ale lui Heisenberg sunt fundamentale pentru tehnologiile cuantice, cum ar 
    fi microscoapele electronice si dispozitivele de imagistica, care se bazeaza pe principiile de 
    difractie si interferenta. De asemenea, ele sunt esentiale in functionarea laserelor cu durata foarte 
    scurta, unde impulsurile scurte de lumina permit studierea proceselor extrem de rapide. Principiul 
    incertitudinii mai este aplicat si in criptografia cuantica si computatia cuantica, unde fluctuatiile 
    energetice si interactiunile de scurta durata sunt utilizate pentru a controla informatiile la nivel cuantic. 
    """)
    append_to_file(RESULTS_FILE, f"""Q: Ce explicatii gasiti daca paramentru k_H se dovedeste a fi neunitar?""")
    append_to_file(RESULTS_FILE, f"""A: Daca parametrul k_H se dovedeste a fi neunitar, acest lucru ar sugera ca exista o discrepanta in 
    masuratorile sau calculele efectuate. In context fizic, neunitatea unui astfel de parametru ar putea 
    indica existenta unor pierderi de energie, disipare sau interactiuni neintentionate cu mediul extern. 
    De asemenea, ar putea sugera necesitatea revizuirii teoriei sau a modelului matematic utilizat pentru 
    a descrie fenomenul, semnaland ca presupunerile initiale nu sunt pe deplin corecte sau ca exista 
    factori aditionali care trebuie luati in considerare.""")


if __name__ == "__main__":
    delete_file(RESULTS_FILE)
    delete_file(MINIMUM_INTENSITY_TABLE_FILE)
    main()
