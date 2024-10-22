from unum import Unum
from unum.units import *


class Constants:
    c: Unum

    def __init__(self):
        self.c = 299_792_458 * m / s

CONSTANTS = Constants()
