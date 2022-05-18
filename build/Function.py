from build.Util import *

class Function:
    def __init__(self, function, point, order, functype, title):
        self.circuit = None
        self.horner_coeffs = None
        self.poli_coeffs = None
        self.taylor_coeffs = None
        self.function = function
        self.point = point
        self.order = order
        self.functype = functype
        self.title = title

    def generateCoeffs(self):
        print("-" * 100)
        print("Taylor Coeffs")
        print("")
        self.taylor_coeffs = make_taylor_coeffs(self)
        for index in self.taylor_coeffs:
            print(index, ": ", self.taylor_coeffs[index])

        print("-" * 100)
        print("Polynomial Coeffs")
        print("")
        self.poli_coeffs = make_polynomial(self)
        for index in self.poli_coeffs:
            print(index, ": ", self.poli_coeffs[index])

        print("-" * 100)
        print("Horner Expansion Coeffs")
        print("")
        self.horner_coeffs = make_horner(self)
        for index in self.horner_coeffs:
            print(index, ": ", self.horner_coeffs[index])

    def generateCircuit(self):
        self.circuit = horner_to_circuit(self)
        show_graph(self)

    def generateReactions(self):
        make_reactions(self.circuit)

    def isSinusoidal(self):
        if self.functype == FuncTypes.SINUSOIDAL:
            return 1
        elif self.functype == FuncTypes.SINE:
            return 1
        elif self.functype == FuncTypes.COSINE:
            return 1
        else:
            return 0

    def isExponential(self):
        if self.functype == FuncTypes.EXPONENTIAL:
            return 1
        else:
            return 0

    def isLogarithmic(self):
        if self.functype == FuncTypes.LOGARITHMIC:
            return 1
        else:
            return 0
