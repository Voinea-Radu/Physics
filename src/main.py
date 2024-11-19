import numpy as np
from prettytable import PrettyTable

from src.utils import write_to_csv
from utils import delete_file
import matplotlib.pyplot as plt


class Specter:
    color_name: str
    intensity: str
    wavelength: float
    x: int

    def __init__(self, color_name: str, intensity: str, wavelength: float, x: int):
        self.color_name = color_name
        self.intensity = intensity
        self.wavelength = wavelength
        self.x = x


class Band:
    x_prime: int
    x_double_prime: int
    lambda_prime: float
    lambda_double_prime: float

    def __init__(self, x_prime: int, x_double_prime: int, lambda_prime: float, lambda_double_prime: float):
        self.x_prime = x_prime
        self.x_double_prime = x_double_prime
        self.lambda_prime = lambda_prime
        self.lambda_double_prime = lambda_double_prime


mercury_specter: list[Specter] = [
    Specter("rosu", "intens", 623.4, 0),
    Specter("roşu", "intens", 612.3, 0),
    Specter("roşu", "intens", 607.3, 0),
    Specter("portocaliu", "slab", 589.0, 0),
    Specter("portocaliu", "foarte slab", 585.9, 0),
    Specter("galben", "foarte intens", 579.0, 0),
    Specter("galben", "foarte intens", 577.0, 0),
    Specter("verde", "foarte intens", 546.1, 0),
    Specter("verde", "slab", 538.5, 0),
    Specter("verde", "slab", 535.4, 0),
    Specter("albastru - verde", " foarteslab", 496.0, 0),
    Specter("albastru - verde", "slab", 491.6, 0),
    Specter("albastru", "foarte intens", 435.8, 0),
    Specter("violet", "intens", 407.8, 0),
    Specter("violet", " foarte intens", 404.7, 0)
]

helium_specter: list[Specter] = [
    Specter("rosu", "intens", 623.4, 0),
    Specter("roşu", "intens", 612.3, 0),
    Specter("roşu", "intens", 607.3, 0),
    Specter("portocaliu", "slab", 589.0, 0),
    Specter("portocaliu", "foarte slab", 585.9, 0),
    Specter("galben", "foarte intens", 579.0, 0),
    Specter("galben", "foarte intens", 577.0, 0),
    Specter("verde", "foarte intens", 546.1, 0),
    Specter("verde", "slab", 538.5, 0),
    Specter("verde", "slab", 535.4, 0),
    Specter("albastru - verde", " foarteslab", 496.0, 0),
    Specter("albastru - verde", "slab", 491.6, 0),
    Specter("albastru", "foarte intens", 435.8, 0),
    Specter("violet", "intens", 407.8, 0),
    Specter("violet", " foarte intens", 404.7, 0)
]

bands: list[Band] = [
    Band(1, 1, 1, 1)
]

# Function to calculate dispersion at specific wavelengths
def calculate_dispersion(specter_list, target_wavelengths):
    specter_list = sorted(specter_list, key=lambda s: s.wavelength)
    wavelengths = [s.wavelength for s in specter_list]
    x_values = [s.x for s in specter_list]

    dispersions = {}
    for target_lambda in target_wavelengths:
        for i in range(len(wavelengths) - 1):
            if wavelengths[i] <= target_lambda <= wavelengths[i + 1]:
                # Linear interpolation to approximate dx/dλ
                slope = (x_values[i + 1] - x_values[i]) / (wavelengths[i + 1] - wavelengths[i])
                dispersions[target_lambda] = 1 / slope  # Inverse of slope
                break
    return dispersions

# Function to plot specter and annotate key points
def plot_specter_with_dispersion(specter_list, dispersions, title):
    wavelengths = [s.wavelength for s in specter_list]
    x_values = [s.x for s in specter_list]
    plt.plot(x_values, wavelengths, marker='o', label="Calibration Curve")
    for target_lambda, dispersion in dispersions.items():
        closest_x = np.interp(target_lambda, wavelengths, x_values)
        plt.scatter(closest_x, target_lambda, color='red', label=f"λ={target_lambda}nm, D={dispersion:.2f}")
    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Wavelength (nm)')
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    mercury_specter_table = PrettyTable()
    helium_specter_table = PrettyTable()
    bands_table = PrettyTable()

    mercury_specter_table.field_names = ["Color Name", "Intensity", "Wavelength", "X"]
    helium_specter_table.field_names = ["Color Name", "Intensity", "Wavelength", "X"]
    bands_table.field_names = ["X' / X''", "lambda'/ lambda''"]

    for specter in mercury_specter:
        mercury_specter_table.add_row([specter.color_name, specter.intensity, specter.wavelength, specter.x])

    for specter in helium_specter:
        helium_specter_table.add_row([specter.color_name, specter.intensity, specter.wavelength, specter.x])

    for band in bands:
        bands_table.add_row([band.x_prime / band.x_double_prime, band.lambda_prime / band.lambda_double_prime])

    write_to_csv("mercury_specter_table.csv", mercury_specter_table)
    write_to_csv("helium_specter_table.csv", helium_specter_table)
    write_to_csv("bands_table.csv", bands_table)

    target_wavelengths = [420, 500, 580]
    dispersions = calculate_dispersion(mercury_specter, target_wavelengths)

    # Display dispersions in a table
    dispersion_table = PrettyTable()
    dispersion_table.field_names = ["Wavelength (nm)", "Dispersion (dx/dλ)"]
    for wavelength, dispersion in dispersions.items():
        dispersion_table.add_row([wavelength, dispersion])
    print(dispersion_table)
    plot_specter_with_dispersion(mercury_specter, dispersions, "Mercury Specter: Dispersion Calculation")



if __name__ == "__main__":
    delete_file("results.txt")
    main()
