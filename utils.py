from prettytable import PrettyTable
from unum import Unum
import os
from unum.units import *

kV = Unum.unit("kV", 1000 * V)  # 1 kV = 1000 V

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


def get_median_and_error(data: list[Unum]) -> tuple[Unum, Unum, float]:
    d1_exp_median = unit_sum(data) / len(data)
    d1_exp_errors = [abs(entry - d1_exp_median) for entry in data]
    d1_exp_error_median = unit_sum(d1_exp_errors) / len(d1_exp_errors)

    error_percentage = (d1_exp_median + d1_exp_error_median) * 100 / d1_exp_median - 100

    return d1_exp_median, d1_exp_error_median, error_percentage.asNumber()


def write_to_csv(file_name:str, table: PrettyTable):
    for row in table._rows:
        for i in range(len(row)):
            if isinstance(row[i], Unum):
                row[i] = float(f"{row[i].asNumber():.2f}")
            if isinstance(row[i], float):
                row[i] = f"{row[i]:.2f}"

    data = table.get_csv_string()

    with open(file_name, "w", encoding="utf-8") as file:
        for line in data.split("\n"):
            file.write(f"{line}")


def delete_file(file_name:str):
    if os.path.exists(file_name):
        os.remove(file_name)

def append_to_file(file_name:str, data:str):
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(data)
        file.write("\n")