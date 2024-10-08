from prettytable import PrettyTable
from unum import Unum


def get_column(table: PrettyTable, label: str) -> list:
    column_index = table.field_names.index(label)
    column_data = [row[column_index] for row in table._rows]
    return column_data


def get_columns(table: PrettyTable, labels: list[str]) -> list:
    to_zip = []

    for label in labels:
        to_zip.append(get_column(table, label))

    return list(zip(*to_zip))

def strip_measurement_units(table:PrettyTable):
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

def get_median_and_error(data: list[Unum]) -> tuple[Unum, Unum]:
    d1_exp_median = unit_sum(data) / len(data)
    d1_exp_errors = [abs(entry - d1_exp_median) for entry in data]
    d1_exp_error_median = unit_sum(d1_exp_errors) / len(d1_exp_errors)
    return d1_exp_median, d1_exp_error_median