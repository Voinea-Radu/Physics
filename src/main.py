import numpy as np
from matplotlib import pyplot as plt
from prettytable import PrettyTable
from unum.units import mm, nm, um, m

from src.utils import write_to_csv, append_to_file, Median
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


if __name__ == "__main__":
    delete_file("results.txt")
    main()
