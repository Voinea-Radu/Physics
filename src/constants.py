from unum.units import m, s, C
from unum import Unum


class Constants:
    c: Unum = 3 * 10 ** 8 * m / s
    e: Unum = 1.6 * 10 ** (-19) * C

    def __init__(self):
        pass


CONSTANTS = Constants()
