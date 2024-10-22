from unum import Unum
from unum.units import mm, cm


class Constants:
    class Order:
        order: int
        epsilon_M: Unum  # Pozitie maxim
        I_n: Unum  # epsilon

        def __init__(self,
                     order: int,
                     epsilon_M: Unum,
                     I_n: Unum,
                     ):
            self.order = order
            self.epsilon_M = epsilon_M
            self.I_n = I_n

    SLOT_A: Unum
    SLOT_B: Unum
    SLOT_C: Unum

    D: Unum

    ORDER_1: Order
    ORDER_2: Order
    ORDER_3: Order

    PI: float

    def __init__(self):
        # Slot sizes for diaphragm 46991
        self.SLOT_A = 0.12 * mm
        self.SLOT_B = 0.24 * mm
        self.SLOT_C = 0.48 * mm

        self.D = 180 * cm

        self.PI = 3.141592653589793238462643383279502884197169399375105820974944

        self.ORDER_1 = Constants.Order(
            order=1,
            epsilon_M=4.493 * mm / mm,
            I_n=0.0472 * mm
        )
        self.ORDER_2 = Constants.Order(
            order=2,
            epsilon_M=7.725 * mm / mm,
            I_n=0.0168 * mm
        )
        self.ORDER_3 = Constants.Order(
            order=3,
            epsilon_M=10.904 * mm / mm,
            I_n=0.00834 * mm
        )

    def get_order(self, order: int) -> Order:
        if order == 1:
            return self.ORDER_1
        if order == 2:
            return self.ORDER_2
        if order == 3:
            return self.ORDER_3
        raise ValueError("Invalid order")


CONSTANTS = Constants()
