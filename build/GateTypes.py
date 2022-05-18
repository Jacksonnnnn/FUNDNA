from enum import Enum


class GateTypes(Enum):
    NAND = "Nand"
    AND = "And"
    BNAND = "Bipolar Nand"
    BAND = "Bipolar And"
    MUX = "MUX"

    def isIn(self):
        if type(self) is str:
            if (self == GateTypes.NAND.value or
                    self == GateTypes.AND.value or
                    self == GateTypes.BNAND.value or
                    self == GateTypes.BAND.value or
                    self == GateTypes.MUX.value):
                return 1
            else:
                return 0
        else:
            if (self == GateTypes.NAND or
                    self == GateTypes.AND or
                    self == GateTypes.BNAND or
                    self == GateTypes.BAND or
                    self == GateTypes.MUX):
                return 1
            else:
                return 0