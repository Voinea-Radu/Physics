from prettytable import PrettyTable
from unum import Unum
from unum.units import mm, nm

from constants import CONSTANTS
from utils import Median


class Slot:
    class Measurement:
        x: Unum
        U_F: Unum

        def __init__(self, x: Unum, U_F: Unum):
            self.x = x
            self.U_F = U_F

    left_minimums: list[Measurement]
    right_minimums: list[Measurement]
    left_maximums: list[Measurement]
    central_maximum: Measurement
    right_maximums: list[Measurement]

    def __init__(self,
                 left_minimums: list[Measurement],
                 right_minimums: list[Measurement],
                 left_maximums: list[Measurement],
                 central_maximum: Measurement,
                 right_maximums: list[Measurement],
                 ):
        self.left_minimums = left_minimums
        self.right_minimums = right_minimums
        self.left_maximums = left_maximums
        self.central_maximum = central_maximum
        self.right_maximums = right_maximums


def compute_lambda(x_mn: Unum, order: int, slot_size: Unum) -> Unum:
    return (x_mn * slot_size) / (CONSTANTS.D * order)


def compute_xmn(x_left: Unum, x_right: Unum) -> Unum:
    return (abs(x_left) + abs(x_right)) / 2


class MinimumIntensityData:
    left_of_central_minimum_3: Unum
    left_of_central_minimum_2: Unum
    left_of_central_minimum_1: Unum
    right_of_central_minimum_1: Unum
    right_of_central_minimum_2: Unum
    right_of_central_minimum_3: Unum

    def __init__(self, slot: Slot):
        self.left_of_central_minimum_3 = slot.left_minimums[0].x
        self.left_of_central_minimum_2 = slot.left_minimums[1].x
        self.left_of_central_minimum_1 = slot.left_minimums[2].x
        self.right_of_central_minimum_1 = slot.right_minimums[0].x
        self.right_of_central_minimum_2 = slot.right_minimums[1].x
        self.right_of_central_minimum_3 = slot.right_minimums[2].x

    def create_table(self) -> PrettyTable:
        table: PrettyTable = PrettyTable()

        table.add_column(
            "C0",
            [
                "Pozitie fata de MC",
                "Ordin minim",
                "Pozitie X Rigla (mm)"
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
        order_id: int
        x_mn: Unum
        lambda_: Unum

        def __init__(self,
                     order_id: int,
                     x_mn: Unum,
                     slot_size: Unum
                     ):
            self.order_id = order_id
            self.x_mn = x_mn
            self.lambda_ = compute_lambda(x_mn, order_id, slot_size).asUnit(nm)

    order_1: Order
    order_2: Order
    order_3: Order

    def __init__(self, data: MinimumIntensityData, slot_size: Unum):
        self.order_1 = MinimumIntensityComputedData.Order(
            1,
            x_mn=compute_xmn(data.left_of_central_minimum_1, data.right_of_central_minimum_1),
            slot_size=slot_size
        )
        self.order_2 = MinimumIntensityComputedData.Order(
            2,
            x_mn=compute_xmn(data.left_of_central_minimum_2, data.right_of_central_minimum_2),
            slot_size=slot_size
        )
        self.order_3 = MinimumIntensityComputedData.Order(
            3,
            x_mn=compute_xmn(data.left_of_central_minimum_3, data.right_of_central_minimum_3),
            slot_size=slot_size
        )

    def get_median(self) -> Median:
        return Median([self.order_1.lambda_, self.order_2.lambda_, self.order_3.lambda_])

    def create_table(self) -> PrettyTable:
        table: PrettyTable = PrettyTable()

        table.add_column(
            "C0",
            [
                "Ordin minim",
                "X_mn",
                "Lambda",
            ]
        )

        table.add_column(
            "C1",
            [
                "1",
                self.order_1.x_mn,
                self.order_1.lambda_,
            ]
        )
        table.add_column(
            "C2",
            [
                "2",
                self.order_2.x_mn,
                self.order_2.lambda_,
            ]
        )
        table.add_column(
            "C3",
            [
                "3",
                self.order_3.x_mn,
                self.order_3.lambda_,
            ]
        )

        return table


class MaximumIntensityData:
    slot_A: Slot
    slot_B: Slot
    slot_C: Slot

    def __init__(self,
                 slot_A: Slot,
                 slot_B: Slot,
                 slot_C: Slot = None,
                 ):
        self.slot_A = slot_A
        self.slot_B = slot_B
        self.slot_C = slot_C

    def create_table(self) -> PrettyTable:
        table: PrettyTable = PrettyTable()

        table.add_column(
            "C0",
            [
                "Pozitie fata de MC",
                "Ordin maxim",
                "Fanta A", None,
                "Fanta B", None,
            ] + (["Fanta C", None, ] if self.slot_C is not None else [])
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
            ] + (["X maxim", "U_F (mv)"] if self.slot_C is not None else [])
        )

        table.add_column(
            "C2",
            [
                "Stanga MC",
                "3",
                self.slot_A.left_maximums[2].x,
                self.slot_A.left_maximums[2].U_F,
                self.slot_B.left_maximums[2].x,
                self.slot_B.left_maximums[2].U_F,

            ] + ([self.slot_C.left_maximums[2].x, self.slot_C.left_maximums[2].U_F] if self.slot_C is not None else [])
        )
        table.add_column(
            "C3",
            [
                "Stanga MC",
                "2",
                self.slot_A.left_maximums[1].x,
                self.slot_A.left_maximums[1].U_F,
                self.slot_B.left_maximums[1].x,
                self.slot_B.left_maximums[1].U_F,
            ] + ([self.slot_C.left_maximums[1].x, self.slot_C.left_maximums[1].U_F] if self.slot_C is not None else [])
        )
        table.add_column(
            "C4",
            [
                "Stanga MC",
                "1",
                self.slot_A.left_maximums[0].x,
                self.slot_A.left_maximums[0].U_F,
                self.slot_B.left_maximums[0].x,
                self.slot_B.left_maximums[0].U_F,
            ] + ([self.slot_C.left_maximums[0].x, self.slot_C.left_maximums[0].U_F] if self.slot_C is not None else [])
        )
        table.add_column(
            "C5",
            [
                "MC",
                None,
                self.slot_A.central_maximum.x,
                self.slot_A.central_maximum.U_F,
                self.slot_B.central_maximum.x,
                self.slot_B.central_maximum.U_F,
            ] + ([self.slot_C.central_maximum.x, self.slot_C.central_maximum.U_F] if self.slot_C is not None else [])
        )
        table.add_column(
            "C6",
            [
                "Dreapta MC",
                "1",
                self.slot_A.right_maximums[0].x,
                self.slot_A.right_maximums[0].U_F,
                self.slot_B.right_maximums[0].x,
                self.slot_B.right_maximums[0].U_F,
            ] + ([self.slot_C.right_maximums[0].x, self.slot_C.right_maximums[0].U_F] if self.slot_C is not None else [])
        )
        table.add_column(
            "C7",
            [
                "Dreapta MC",
                "2",
                self.slot_A.right_maximums[1].x,
                self.slot_A.right_maximums[1].U_F,
                self.slot_B.right_maximums[1].x,
                self.slot_B.right_maximums[1].U_F,
            ] + ([self.slot_C.right_maximums[1].x, self.slot_C.right_maximums[1].U_F] if self.slot_C is not None else [])
        )
        table.add_column(
            "C8",
            [
                "Dreapta MC",
                "3",
                self.slot_A.right_maximums[2].x,
                self.slot_A.right_maximums[2].U_F,
                self.slot_B.right_maximums[2].x,
                self.slot_B.right_maximums[2].U_F,
            ] + ([self.slot_C.right_maximums[2].x, self.slot_C.right_maximums[2].U_F] if self.slot_C is not None else [])
        )

        return table


class MaximumIntensityComputedData:
    class Slot:
        class Order:
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
                self.X_Mne = compute_xmn(X_left, X_right)

                self.X_Mnt = ((lambda_ * CONSTANTS.D * CONSTANTS.get_order(order_id).epsilon_M) / (CONSTANTS.PI * slot_size)).asUnit(mm)
                self.k_xM = self.X_Mne / self.X_Mnt

                epsilon_m = (CONSTANTS.PI * slot_size * self.X_Mne) / (lambda_ * CONSTANTS.D)
                print(epsilon_m)

                from math import sin
                self.I_ne = (sin(epsilon_m) ** 2) / (epsilon_m ** 2)  # TODO
                self.k_I = self.I_ne / CONSTANTS.get_order(order_id).I_n

                self.I_ne = f"{self.I_ne.asNumber():.6f}"

        order_1: Order
        order_2: Order
        order_3: Order

        def __init__(self,
                     slot: Slot,
                     lambda_: Unum,
                     slot_size: Unum,
                     ):
            self.order_1 = MaximumIntensityComputedData.Slot.Order(
                order_id=1,
                X_left=slot.left_maximums[0].x,
                X_right=slot.right_maximums[0].x,
                lambda_=lambda_,
                slot_size=slot_size,
            )
            self.order_2 = MaximumIntensityComputedData.Slot.Order(
                order_id=2,
                X_left=slot.left_maximums[1].x,
                X_right=slot.right_maximums[1].x,
                lambda_=lambda_,
                slot_size=slot_size,
            )
            self.order_3 = MaximumIntensityComputedData.Slot.Order(
                order_id=3,
                X_left=slot.left_maximums[2].x,
                X_right=slot.right_maximums[2].x,
                lambda_=lambda_,
                slot_size=slot_size,
            )

    slot_A: Slot
    slot_B: Slot
    slot_C: Slot

    def __init__(self,
                 lambda_: Unum,
                 slot_A: Slot,
                 slot_B: Slot,
                 slot_C: Slot = None,
                 ):
        self.slot_A = MaximumIntensityComputedData.Slot(
            slot=slot_A,
            lambda_=lambda_,
            slot_size=CONSTANTS.SLOT_A
        )
        self.slot_B = MaximumIntensityComputedData.Slot(
            slot=slot_B,
            lambda_=lambda_,
            slot_size=CONSTANTS.SLOT_B
        )
        if slot_C is not None:
            self.slot_C = MaximumIntensityComputedData.Slot(
                slot=slot_C,
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
                "X_Mne (mm)",
                "X_Mnt (mm)",
                "k_xM",
                "I_ne",
                "k_I",
            ]
        )

        for (index, slot) in enumerate([self.slot_A, self.slot_B] + ([self.slot_C] if hasattr(self, "slot_C") else [])):
            table.add_column(
                "C1",
                [
                    "Fanta " + chr(ord("A") + index),
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
                    "Fanta " + chr(ord("A") + index),
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
                    "Fanta " + chr(ord("A") + index),
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
                 lambda_: Unum,
                 slot_A_left: list[Unum],
                 slot_A_right: list[Unum],
                 slot_B_left: list[Unum],
                 slot_B_right: list[Unum],
                 slot_C_left: list[Unum] = None,
                 slot_C_right: list[Unum] = None,
                 ):
        self.slot_A_left = slot_A_left
        self.slot_A_right = slot_A_right
        self.slot_B_left = slot_B_left
        self.slot_B_right = slot_B_right

        if slot_C_left is not None and slot_C_right is not None:
            self.slot_C_left = slot_C_left
            self.slot_C_right = slot_C_right

        self.compute(lambda_)

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
        if hasattr(self, "slot_C_left") and hasattr(self, "slot_C_right"):
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

        for (index, slot) in enumerate([self.slot_A, self.slot_B] + ([self.slot_C] if hasattr(self, "slot_C") else [])):
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
