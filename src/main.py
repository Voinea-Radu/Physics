import numpy as np
from matplotlib import pyplot as plt
from numpy.ma.core import append
from prettytable import PrettyTable
from unum.units import mm, nm, um, m

from utils import write_to_csv, append_to_file, Median
from utils import delete_file


def main():
    mercury_spectrogram = PrettyTable()


    zero = 49.5 * mm


    lambda_list = [623.4, 612.3, 579.0, 577.0, 546.1, 535.4, 435.8, 434.7, 433.9, 407.8, 404.7] * nm
    x_list = [34.5, 33.8, 29.9, 29.5, 29, 16.5, 15.1, 13, 12.5, 9.9, 9.2] * mm
    x_list = [zero-x for x in x_list]
    x_list = x_list[::-1]
    one_over_lambda_squared_list = [1 / ((l ** 2).asUnit(um ** 2)) for l in lambda_list]

    # plot lambda vs x
    plt.plot([x.asNumber() for x in x_list], [l.asNumber() for l in lambda_list], marker='o', linestyle='-', color='b')
    plt.ylabel('Wavelength (nm)')
    plt.xlabel('Position (mm)')
    plt.title('Lambda vs X')
    plt.grid(True)
    plt.savefig('lambda_vs_x.png')
    plt.show()

    # plot 1/lambda^2 vs x
    slope, intercept = np.polyfit([x.asNumber() for x in x_list], [l.asNumber() for l in one_over_lambda_squared_list], 1)
    D1_pred = slope * np.array([x.asNumber() for x in x_list]) + intercept
    print(D1_pred)

    plt.plot([x.asNumber() for x in x_list], D1_pred, color="red", label=f"Linear Fit: y = {slope:.2f}x + {intercept:.2f}")
    plt.plot([x.asNumber() for x in x_list], [l.asNumber() for l in one_over_lambda_squared_list], marker='o', linestyle='-', color='b')
    plt.ylabel('1/lambda^2 (1/um^2)')
    plt.xlabel('Position (mm)')
    plt.title('1/Lambda^2 vs X')
    plt.grid(True)
    plt.savefig('1_lambda_squared_vs_x.png')
    plt.show()

    mercury_spectrogram.field_names = ["lambda (nm)", "x (mm)", "1/lambda^2 (1/um^2)"]
    for lambda_, x, one_over_lambda_squared in zip(lambda_list, x_list, one_over_lambda_squared_list):
        mercury_spectrogram.add_row([lambda_, x, one_over_lambda_squared])

    write_to_csv("mercury_spectrogram.csv", mercury_spectrogram)

    rydberg = PrettyTable()

    zero = 49.8 * mm

    x_list = [46, 36.5, 33.5, 29.7, 21.5, 6.7] * mm
    x_list = [zero - x for x in x_list]
    x_list = x_list[::-1]
    n_list = [3, 4, 5, 6, 7, 8]
    lines = ["H_alpha", "H_beta", "H_gamma", "H_delta", "H_epsilon", "H_infinity"]
    R_H_list = []

    rydberg.field_names = ["Lina", "x (mm)", "1/lambda^2 (1/um^2)", "lambda (nm)", "n", "R_H"]
    for line, x, n in zip(lines, x_list, n_list):
        one_over_lambda_squared = (slope * x.asNumber() + intercept) * (1 / um ** 2)
        lambda_ = (1 / one_over_lambda_squared ** (1 / 2)).asUnit(nm)
        R_H = ((4 * n ** 2) / (lambda_ * (n ** 2 - 4))).asUnit(1 / m)
        R_H_list.append(R_H)
        rydberg.add_row([line, x, one_over_lambda_squared, lambda_, n, R_H])

    write_to_csv("rydberg.csv", rydberg)

    R_H_median = Median(R_H_list)
    append_to_file("results.txt", f"R_H_median: {R_H_median.median.asNumber():.0f} +- {R_H_median.square_deviation.asNumber():.0f} 1/m")
    append_to_file("results.txt", """
1. **Ce sunt liniile spectrale?**  
   Liniile spectrale reprezintă radiația emisă sau absorbită de atomi, molecule sau ioni atunci când electronii lor se mută între diferite nivele energetice. Aceste linii apar ca niște benzi de lumină distincte într-un spectru și sunt specifice fiecărui element, având frecvențe și lungimi de undă precise.

2. **Ce este lungimea de undă? Dar numărul de undă? În ce relație se găsesc acestea cu frecvența radiației? Dar cu energia radiației?**  
   Lungimea de undă (\(\lambda\)) este distanța dintre două puncte succesive într-o undă, de exemplu între două creste consecutive. Numărul de undă (\(\tilde{\nu}\)) este inversul lungimii de undă (\(\tilde{\nu} = \frac{1}{\lambda}\)) și se măsoară în cm⁻¹.  
   Relația cu frecvența (\(f\)) este dată de ecuația: \(c = \lambda \cdot f\), unde \(c\) este viteza luminii.  
   Energia radiației (\(E\)) este legată de frecvență prin formula \(E = h \cdot f\), unde \(h\) este constanta Planck.

3. **Ce este o serie spectrală a hidrogenului? Câte linii spectrale conține o serie spectrală? Care este limita unei serii spectrale? Care este energia nivelului superior al tranziției corespunzătoare limitei seriei spectrale? Dar numărul său cuantic principal?**  
   Seria spectrală a hidrogenului constă în grupuri de linii spectrale generate de tranzițiile electronilor între niveluri energetice discrete. Cele mai cunoscute serii spectrale sunt seria Lyman, Balmer, Paschen, Brackett și Pfund, fiecare caracterizată prin tranziții către un anumit nivel energetic final.  
   Limita unei serii spectrale este valoarea frecvenței sau a lungimii de undă la care liniile spectrale converg, corespunzătoare tranzițiilor de la nivele energetice superioare către un nivel fix. Energia nivelului superior la limită este considerată infinită, iar numărul cuantic principal \(n\) este infinit.

4. **Ce este un termen spectral?**  
   Un termen spectral este energia unui anumit nivel energetic al unui atom, exprimată de obicei în cm⁻¹. Termenii spectrali sunt folosiți pentru a calcula diferențele de energie între nivele și sunt folosiți frecvent în analiza spectrelor atomice.

5. **Ce reprezintă principiul de combinare Rydberg-Ritz în studiul liniilor spectrale emise de atomi? Care este utilitatea lui? Ce este mai simplu (sau mai comod) de cunoscut: liniile spectrale sau termenii spectrali? Justificați răspunsul.**  
   Principiul de combinare Rydberg-Ritz afirmă că diferențele dintre termeni spectrali (energie) corespund liniilor spectrale observabile. Utilitatea acestui principiu constă în posibilitatea de a prezice liniile spectrale pe baza termenilor spectrali cunoscuți. Termenii spectrali sunt mai convenabili de cunoscut, deoarece permit o înțelegere mai sistematică și simplifică calculul liniilor spectrale.

6. **Ce sunt atomii hidrogenoizi?**  
   Atomii hidrogenoizi sunt atomi sau ioni cu un singur electron, similar atomului de hidrogen. Exemple de astfel de specii sunt ionii He⁺, Li²⁺ și Be³⁺. Acești atomi prezintă un spectru similar cu cel al hidrogenului, deoarece interacțiunea electromagnetică este similară, având un singur electron legat de nucleu.

7. **Care au fost postulatele enunțate de Bohr pentru explicarea spectrului atomilor de hidrogen?**  
   Postulatele lui Bohr sunt:
   - Electronii se mișcă pe orbite circulare stabile în jurul nucleului fără a emite radiație.
   - Numai anumite orbite sunt permise, iar momentul cinetic al electronului este cuantificat.
   - Emisia sau absorbția radiației are loc numai atunci când electronul trece de la o orbită permisă la alta, energia radiației fiind egală cu diferența de energie între cele două nivele.

8. **Să se aranjeze în ordinea crescătoare a lungimilor de undă liniile spectrale: \( H_\alpha, H_\beta, H_\gamma, H_\delta, H_\epsilon, H_\zeta \) și \( H_\infty \).**  
   Ordinea crescătoare a lungimilor de undă este:
   - \( H_\infty \), \( H_\zeta \), \( H_\epsilon \), \( H_\delta \), \( H_\gamma \), \( H_\beta \), \( H_\alpha \).  
   (Aceasta este ordinea frecvențelor în seria Balmer, de la cea mai mare la cea mai mică lungime de undă.)

9. **Ce este o spectrogramă? Ce este curba de etalonare a spectrogramei? La ce folosește curba de etalonare a spectrogramei?**  
   O spectrogramă este o înregistrare a intensității luminii în funcție de lungimea de undă, obținută de la un spectroscop. Curba de etalonare este o funcție folosită pentru a converti măsurătorile spectrografice brute în valori corecte de lungime de undă. Aceasta este esențială pentru a asigura precizia în interpretarea spectrelor și identificarea corectă a elementelor.

Pentru a rezolva aceste probleme, putem folosi formula dată pentru a determina constanta lui Rydberg (\( R_H \)).

### 10. Determinarea constantei lui Rydberg folosind linia \( H_\beta \) din seria Balmer

Avem:
- Lungimea de undă \( \lambda_{H_\beta} = 486 \) nm.
- \( n = 4 \) pentru linia \( H_\beta \) din seria Balmer (seria Balmer implică tranziții către \( n = 2 \)).

Formula este:
\[
\tilde{\nu}_n = \frac{1}{\lambda_n} = R_H \left( \frac{1}{2^2} - \frac{1}{n^2} \right)
\]

Înlocuim valorile:
\[
\frac{1}{486 \text{ nm}} = R_H \left( \frac{1}{4} - \frac{1}{16} \right)
\]

Calculăm:
\[
\frac{1}{486 \times 10^{-9} \text{ m}} = R_H \cdot \left( \frac{4 - 1}{16} \right)
\]

### 11. Determinarea constantei lui Rydberg folosind limita seriei Balmer

Avem:
- Lungimea de undă \( \lambda_{\infty} = 364,6 \) nm (limita seriei Balmer).
- Pentru limita seriei Balmer, \( n \rightarrow \infty \), deci termenul \( \frac{1}{n^2} \rightarrow 0 \).

Formula devine:
\[
\tilde{\nu}_\infty = \frac{1}{\lambda_\infty} = R_H \cdot \frac{1}{2^2}
\]

Înlocuim valorile:
\[
\frac{1}{364,6 \times 10^{-9} \text{ m}} = R_H \cdot \frac{1}{4}
\]

Rezolvăm fiecare ecuație pentru \( R_H \) în funcție de lungimile de undă date pentru a găsi valoarea constantei lui Rydberg. Vrei să efectuez aceste calcule?
    
    
    """)


if __name__ == "__main__":
    delete_file("results.txt")
    main()
