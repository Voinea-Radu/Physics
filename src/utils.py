from prettytable import PrettyTable
from unum import Unum
import os

from unum.units import T, eV

# imp = Unum.unit("imp")
# mT = Unum.unit("mT", T / 1000)
# keV = Unum.unit("keV", T * eV)

def get_column(table: PrettyTable, label: str) -> list:
    column_index = table.field_names.index(label)
    column_data = [row[column_index] for row in table._rows]
    return column_data


def get_columns(table: PrettyTable, labels: list[str]) -> list:
    to_zip = []

    for label in labels:
        to_zip.append(get_column(table, label))

    return list(zip(*to_zip))


def strip_measurement_units(table: PrettyTable):
    for row in table._rows:
        for i in range(len(row)):
            if isinstance(row[i], Unum):
                row[i] = row[i].asNumber()
    return table


def unit_sum(data: list[Unum]) -> Unum:
    output = data[0]

    for index in range(1, len(data)):
        output += data[index]

    return output


def write_to_csv(file_name: str, table: PrettyTable, number_of_decimals:int = 2):
    for row in table._rows:
        for i in range(len(row)):
            if isinstance(row[i], Unum):
                row[i] = float(f"{row[i].asNumber():.{number_of_decimals}f}")
            if isinstance(row[i], float):
                row[i] = f"{row[i]:.{number_of_decimals}f}"

    data = table.get_csv_string()
    print(table)

    with open(file_name, "w", encoding="utf-8") as file:
        for line in data.split("\n"):
            file.write(f"{line}")


def delete_file(file_name: str):
    if os.path.exists(file_name):
        os.remove(file_name)


def append_to_file(file_name: str, data: str):
    print(data)
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(data)
        file.write("\n")


class Median:
    median: Unum
    square_deviation: Unum

    def __init__(self, data: list[Unum]):
        self.median = unit_sum(data) / len(data)
        self.square_deviation = (unit_sum([abs(entry - self.median) ** 2 for entry in data]) / len(data)) ** (1 / 2)
