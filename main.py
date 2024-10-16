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
    lambda_=0 * nm,
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
