from prettytable import PrettyTable
from unum import Unum
from unum.units import *

from constants import CONSTANTS
from utils import Median


def compute_lambda(x_mn: Unum, order: int) -> Unum:
    return (x_mn * CONSTANTS.SLOT_C) / (CONSTANTS.D * order)


class MinimumIntensityData:
    left_of_central_minimum_3: Unum # List of 3 measurements
    left_of_central_minimum_2: Unum  # List of 3 measurements
    left_of_central_minimum_1: Unum  # List of 3 measurements
    right_of_central_minimum_1: Unum  # List of 3 measurements
    right_of_central_minimum_2: Unum  # List of 3 measurements
    right_of_central_minimum_3: Unum  # List of 3 measurements

    def __init__(self,
                 left_of_central_minimum_3: Unum,
                 left_of_central_minimum_2: Unum,
                 left_of_central_minimum_1: Unum,
                 right_of_central_minimum_1: Unum,
                 right_of_central_minimum_2: Unum,
                 right_of_central_minimum_3: Unum,
                 ):
        self.left_of_central_minimum_3 = left_of_central_minimum_3
        self.left_of_central_minimum_2 = left_of_central_minimum_2
        self.left_of_central_minimum_1 = left_of_central_minimum_1
        self.right_of_central_minimum_1 = right_of_central_minimum_1
        self.right_of_central_minimum_2 = right_of_central_minimum_2
        self.right_of_central_minimum_3 = right_of_central_minimum_3

    def create_table(self) -> PrettyTable:
        table: PrettyTable = PrettyTable()

        table.add_column(
            "C0",
            [
                "Pozitie fata de MC",
                "Ordin minim",
                "Pozitie X Rigla"
            ]
        )

        table.add_column(
            "C3",
            [
                "Stanga MC",
                "3",
                self.left_of_central_minimum_3
            ]
        )

        table.add_column(
            "C4",
            [
                "Stanga MC",
                "2",
                self.left_of_central_minimum_2,
            ]
        )

        table.add_column(
            "C5",
            [
                "Stanga MC",
                "1",
                self.left_of_central_minimum_1,
            ]
        )

        table.add_column(
            "C6",
            [
                "Dreapta MC",
                "1",
                self.right_of_central_minimum_1,
            ]
        )

        table.add_column(
            "C7",
            [
                "Dreapta MC",
                "2",
                self.right_of_central_minimum_2,
            ]
        )

        table.add_column(
            "C8",
            [
                "Dreapta MC",
                "3",
                self.right_of_central_minimum_3,
            ]
        )

        return table


class MinimumIntensityComputedData:
    class Order:
        order_id: int  # List of 3 measurements
        x_mn: list[Unum]  # List of 3 measurements
        lambda_: list[Unum]  # List of 3 measurements

        def __init__(self,
                     order_id: int,  # 1, 2, 3
                     x_mn: list[Unum],
                     ):
            self.order_id = order_id
            self.x_mn = x_mn
            self.lambda_ = [compute_lambda(x_mn, order_id).asUnit(nm) for x_mn in x_mn]

    order_1: Order
    order_2: Order
    order_3: Order

    def compute_xmn(self, x_left: Unum, x_right: Unum) -> Unum:
        return abs((x_left + x_right) / 2)

    def compute_xmn_list(self, x_left_list: list[Unum], x_right_list: list[Unum]) -> list[Unum]:
        return [self.compute_xmn(x_left, x_right) for x_left, x_right in zip(x_left_list, x_right_list)]

    def __init__(self, data: MinimumIntensityData):
        self.order_1 = MinimumIntensityComputedData.Order(
            1,
            x_mn=self.compute_xmn_list(data.left_of_central_minimum_1, data.right_of_central_minimum_1),
        )
        self.order_2 = MinimumIntensityComputedData.Order(
            2,
            x_mn=self.compute_xmn_list(data.left_of_central_minimum_2, data.right_of_central_minimum_2),
        )
        self.order_3 = MinimumIntensityComputedData.Order(
            3,
            x_mn=self.compute_xmn_list(data.left_of_central_minimum_3, data.right_of_central_minimum_3),
        )

    def get_median(self) -> Median:
        return Median(self.order_1.lambda_ + self.order_2.lambda_ + self.order_3.lambda_)

    def create_table(self) -> PrettyTable:
        table: PrettyTable = PrettyTable()

        table.add_column(
            "C0",
            [
                None,
                "Ordin minim",
                "X_mn",
                "Lambda",
            ]
        )

        for measurement in range(3):
            table.add_column(
                "C" + str(measurement * 3 + 1),
                [
                    "Masuratoarea " + str(measurement + 1),
                    "1",
                    self.order_1.x_mn[measurement],
                    self.order_1.lambda_[measurement],
                ]
            )
            table.add_column(
                "C" + str(measurement * 3 + 2),
                [
                    "Masuratoarea " + str(measurement + 1),
                    "2",
                    self.order_2.x_mn[measurement],
                    self.order_2.lambda_[measurement],
                ]
            )
            table.add_column(
                "C" + str(measurement * 3 + 3),
                [
                    "Masuratoarea " + str(measurement + 1),
                    "3",
                    self.order_3.x_mn[measurement],
                    self.order_3.lambda_[measurement],
                ]
            )

        return table


class MaximumIntensityData:
    class Measurement:
        class Slot:
            maximum_x: Unum
            U_F: Unum

            def __init__(self, x: Unum, U_F: Unum):
                self.maximum_x = x
                self.U_F = U_F

        slot_A: Slot
        slot_B: Slot
        slot_C: Slot

        def __init__(self,
                     slot_A: Slot,
                     slot_B: Slot,
                     slot_C: Slot,
                     ):
            self.slot_A = slot_A
            self.slot_B = slot_B
            self.slot_C = slot_C

    left_of_central_maximum_3: Measurement
    left_of_central_maximum_2: Measurement
    left_of_central_maximum_1: Measurement
    central_maximum: Measurement
    right_of_central_maximum_1: Measurement
    right_of_central_maximum_2: Measurement
    right_of_central_maximum_3: Measurement

    def __init__(self,
                 left_of_central_maximum_3: Measurement,
                 left_of_central_maximum_2: Measurement,
                 left_of_central_maximum_1: Measurement,
                 central_maximum: Measurement,
                 right_of_central_maximum_1: Measurement,
                 right_of_central_maximum_2: Measurement,
                 right_of_central_maximum_3: Measurement,
                 ):
        self.left_of_central_maximum_3 = left_of_central_maximum_3
        self.left_of_central_maximum_2 = left_of_central_maximum_2
        self.left_of_central_maximum_1 = left_of_central_maximum_1
        self.central_maximum = central_maximum
        self.right_of_central_maximum_1 = right_of_central_maximum_1
        self.right_of_central_maximum_2 = right_of_central_maximum_2
        self.right_of_central_maximum_3 = right_of_central_maximum_3

    def create_table(self) -> PrettyTable:
        table: PrettyTable = PrettyTable()

        table.add_column(
            "C0",
            [
                "Pozitie fata de MC",
                "Ordin maxim",
                "Fanta A", None,
                "Fanta B", None,
                "Fanta C", None,
            ]
        )

        table.add_column(
            "C1",
            [
                None,
                None,
                "X maxim",
                "U_F (mv)",
                "X maxim",
                "U_F (mv)",
                "X maxim",
                "U_F (mv)",
            ]
        )

        table.add_column(
            "C2",
            [
                "Stanga MC",
                "3",
                self.left_of_central_maximum_3.slot_A.maximum_x,
                self.left_of_central_maximum_3.slot_A.U_F,
                self.left_of_central_maximum_3.slot_B.maximum_x,
                self.left_of_central_maximum_3.slot_B.U_F,
                self.left_of_central_maximum_3.slot_C.maximum_x,
                self.left_of_central_maximum_3.slot_C.U_F,
            ]
        )
        table.add_column(
            "C3",
            [
                "Stanga MC",
                "2",
                self.left_of_central_maximum_2.slot_A.maximum_x,
                self.left_of_central_maximum_2.slot_A.U_F,
                self.left_of_central_maximum_2.slot_B.maximum_x,
                self.left_of_central_maximum_2.slot_B.U_F,
                self.left_of_central_maximum_2.slot_C.maximum_x,
                self.left_of_central_maximum_2.slot_C.U_F,
            ]
        )
        table.add_column(
            "C4",
            [
                "Stanga MC",
                "1",
                self.left_of_central_maximum_1.slot_A.maximum_x,
                self.left_of_central_maximum_1.slot_A.U_F,
                self.left_of_central_maximum_1.slot_B.maximum_x,
                self.left_of_central_maximum_1.slot_B.U_F,
                self.left_of_central_maximum_1.slot_C.maximum_x,
                self.left_of_central_maximum_1.slot_C.U_F,
            ]
        )
        table.add_column(
            "C5",
            [
                "MC",
                None,
                self.central_maximum.slot_A.maximum_x,
                self.central_maximum.slot_A.U_F,
                self.central_maximum.slot_B.maximum_x,
                self.central_maximum.slot_B.U_F,
                self.central_maximum.slot_C.maximum_x,
                self.central_maximum.slot_C.U_F,
            ]
        )
        table.add_column(
            "C6",
            [
                "Dreapta MC",
                "1",
                self.right_of_central_maximum_1.slot_A.maximum_x,
                self.right_of_central_maximum_1.slot_A.U_F,
                self.right_of_central_maximum_1.slot_B.maximum_x,
                self.right_of_central_maximum_1.slot_B.U_F,
                self.right_of_central_maximum_1.slot_C.maximum_x,
                self.right_of_central_maximum_1.slot_C.U_F,
            ]
        )
        table.add_column(
            "C7",
            [
                "Dreapta MC",
                "2",
                self.right_of_central_maximum_2.slot_A.maximum_x,
                self.right_of_central_maximum_2.slot_A.U_F,
                self.right_of_central_maximum_2.slot_B.maximum_x,
                self.right_of_central_maximum_2.slot_B.U_F,
                self.right_of_central_maximum_2.slot_C.maximum_x,
                self.right_of_central_maximum_2.slot_C.U_F,
            ]
        )
        table.add_column(
            "C8",
            [
                "Dreapta MC",
                "3",
                self.right_of_central_maximum_3.slot_A.maximum_x,
                self.right_of_central_maximum_3.slot_A.U_F,
                self.right_of_central_maximum_3.slot_B.maximum_x,
                self.right_of_central_maximum_3.slot_B.U_F,
                self.right_of_central_maximum_3.slot_C.maximum_x,
                self.right_of_central_maximum_3.slot_C.U_F,
            ]
        )

        return table


class MaximumIntensityComputedData:
    class Slot:
        class Order:
            order_number: int
            X_Mne: Unum
            X_Mnt: Unum
            k_xM: Unum
            I_ne: Unum
            k_I: Unum

            def __init__(self,
                         order_id: int,
                         X_left: Unum,
                         X_right: Unum,
                         lambda_: Unum,

                         slot_size: Unum,
                         ):
                self.order_number = order_id
                self.X_Mne = abs((X_left - X_right) / 2)

                self.X_Mnt = (lambda_ * CONSTANTS.D * CONSTANTS.get_order(order_id).epsilon_M) / (CONSTANTS.PI * slot_size)
                self.k_xM = self.X_Mne / self.X_Mnt

                self.I_ne = 0 * mm / mm  # TODO
                self.k_I = self.I_ne / CONSTANTS.get_order(order_id).I_n

        order_1: Order
        order_2: Order
        order_3: Order

        def __init__(self,
                     slot_left: list[MaximumIntensityData.Measurement.Slot],
                     slot_right: list[MaximumIntensityData.Measurement.Slot],
                     lambda_: Unum,
                     slot_size: Unum,
                     ):
            self.order_1 = MaximumIntensityComputedData.Slot.Order(
                order_id=1,
                X_left=slot_left[0].maximum_x,
                X_right=slot_right[0].maximum_x,
                lambda_=lambda_,
                slot_size=slot_size,
            )
            self.order_2 = MaximumIntensityComputedData.Slot.Order(
                order_id=2,
                X_left=slot_left[1].maximum_x,
                X_right=slot_right[1].maximum_x,
                lambda_=lambda_,
                slot_size=slot_size,
            )
            self.order_3 = MaximumIntensityComputedData.Slot.Order(
                order_id=3,
                X_left=slot_left[2].maximum_x,
                X_right=slot_right[2].maximum_x,
                lambda_=lambda_,
                slot_size=slot_size,
            )

    slot_A: Slot
    slot_B: Slot
    slot_C: Slot

    def __init__(self,
                 data: MaximumIntensityData,
                 lambda_: Unum
                 ):
        self.slot_A = MaximumIntensityComputedData.Slot(
            slot_left=[
                data.left_of_central_maximum_1.slot_A,
                data.left_of_central_maximum_2.slot_A,
                data.left_of_central_maximum_3.slot_A,
            ],
            slot_right=[
                data.right_of_central_maximum_1.slot_A,
                data.right_of_central_maximum_2.slot_A,
                data.right_of_central_maximum_3.slot_A,
            ],
            lambda_=lambda_,
            slot_size=CONSTANTS.SLOT_A
        )
        self.slot_B = MaximumIntensityComputedData.Slot(
            slot_left=[
                data.left_of_central_maximum_1.slot_B,
                data.left_of_central_maximum_2.slot_B,
                data.left_of_central_maximum_3.slot_B,
            ],
            slot_right=[
                data.right_of_central_maximum_1.slot_B,
                data.right_of_central_maximum_2.slot_B,
                data.right_of_central_maximum_3.slot_B,
            ],
            lambda_=lambda_,
            slot_size=CONSTANTS.SLOT_B
        )
        self.slot_C = MaximumIntensityComputedData.Slot(
            slot_left=[
                data.left_of_central_maximum_1.slot_C,
                data.left_of_central_maximum_2.slot_C,
                data.left_of_central_maximum_3.slot_C,
            ],
            slot_right=[
                data.right_of_central_maximum_1.slot_C,
                data.right_of_central_maximum_2.slot_C,
                data.right_of_central_maximum_3.slot_C,
            ],
            lambda_=lambda_,
            slot_size=CONSTANTS.SLOT_C
        )

    def create_table(self) -> PrettyTable:
        table = PrettyTable()

        table.add_column(
            "C0",
            [
                None,
                "Ordin maxim",
                "X_Mne",
                "X_Mnt",
                "k_xM",
                "I_ne",
                "k_I",
            ]
        )

        for slot in [self.slot_A, self.slot_B, self.slot_C]:
            table.add_column(
                "C1",
                [
                    "Fanta A",
                    "1",
                    slot.order_1.X_Mne,
                    slot.order_1.X_Mnt,
                    slot.order_1.k_xM,
                    slot.order_1.I_ne,
                    slot.order_1.k_I,
                ]
            )
            table.add_column(
                "C2",
                [
                    "Fanta A",
                    "2",
                    slot.order_2.X_Mne,
                    slot.order_2.X_Mnt,
                    slot.order_2.k_xM,
                    slot.order_2.I_ne,
                    slot.order_2.k_I,
                ]
            )
            table.add_column(
                "C3",
                [
                    "Fanta A",
                    "3",
                    slot.order_3.X_Mne,
                    slot.order_3.X_Mnt,
                    slot.order_3.k_xM,
                    slot.order_3.I_ne,
                    slot.order_3.k_I,
                ]
            )

        return table


class HeisenbergData:
    class Slot:
        left: list[Unum]  # List of 4 measurements
        right: list[Unum]  # List of 4 measurements
        x_m: list[Unum]
        k_H: list[Unum]

        def __init__(self,
                     left: list[Unum],
                     right: list[Unum],
                     slot_size: Unum,
                     lambda_: Unum
                     ):
            self.left = left
            self.right = right

            self.x_m = [abs((left - right) / 2) for left, right in zip(left, right)]
            self.k_H = [(x_m * slot_size) / (CONSTANTS.D * lambda_) for x_m in self.x_m]

    slot_A: Slot
    slot_B: Slot
    slot_C: Slot

    def __init__(self,
                 slot_A_left: list[Unum],
                 slot_A_right: list[Unum],
                 slot_B_left: list[Unum],
                 slot_B_right: list[Unum],
                 slot_C_left: list[Unum],
                 slot_C_right: list[Unum],
                 lambda_: Unum
                 ):
        self.slot_A_left = slot_A_left
        self.slot_A_right = slot_A_right
        self.slot_B_left = slot_B_left
        self.slot_B_right = slot_B_right
        self.slot_C_left = slot_C_left
        self.slot_C_right = slot_C_right

    def compute(self, lambda_: Unum):
        self.slot_A = HeisenbergData.Slot(
            self.slot_A_left,
            self.slot_A_right,
            CONSTANTS.SLOT_A,
            lambda_
        )
        self.slot_B = HeisenbergData.Slot(
            self.slot_B_left,
            self.slot_B_right,
            CONSTANTS.SLOT_B,
            lambda_
        )
        self.slot_C = HeisenbergData.Slot(
            self.slot_C_left,
            self.slot_C_right,
            CONSTANTS.SLOT_C,
            lambda_
        )

    def create_table(self) -> PrettyTable:
        table = PrettyTable()

        table.add_column(
            "C0",
            [
                "Fanta",
                "Numarul Masuratorii",
                "X_s",
                "X_d",
                "X_m (mm)",
                "k_H",
            ]
        )

        for (index, slot) in enumerate([self.slot_A, self.slot_B, self.slot_C]):
            table.add_column(
                "C1",
                [
                    "Fanta " + chr(ord("A") + index),
                    "1",
                    slot.left[0],
                    slot.right[0],
                    slot.x_m[0],
                    slot.k_H[0],
                ]
            )
            table.add_column(
                "C2",
                [
                    "Fanta " + chr(ord("A") + index),
                    "2",
                    slot.left[1],
                    slot.right[1],
                    slot.x_m[1],
                    slot.k_H[1],
                ]
            )
            table.add_column(
                "C3",
                [
                    "Fanta " + chr(ord("A") + index),
                    "3",
                    slot.left[2],
                    slot.right[2],
                    slot.x_m[2],
                    slot.k_H[2],
                ]
            )
            table.add_column(
                "C4",
                [
                    "Fanta " + chr(ord("A") + index),
                    "4",
                    slot.left[3],
                    slot.right[3],
                    slot.x_m[3],
                    slot.k_H[3],
                ]
            )

        return table
