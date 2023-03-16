from collections import defaultdict
from math import factorial

import matplotlib.pyplot as plt
import networkx as nx
from scipy.misc import derivative
from scipy.special import comb

from FuncTypes import FuncTypes
from GateTypes import GateTypes
from NotGateTypes import NotGateTypes


def taylorToPolyStr(func, forceX):
    polynomial = ""
    if forceX:
        variable = "x"
    else:
        variable = func.variable

    for index in func.poli_coeffs:
        exponent = index
        coeff = round(float(func.poli_coeffs[index]), 4)

        if exponent == 0:
            polynomial = polynomial + str(coeff) + " + "
            continue

        if exponent == 1:
            polynomial = polynomial + str(coeff) + "*" + variable + " + "
            continue

        polynomial = polynomial + str(coeff) + "*" + variable + "^(" + str(exponent) + ") + "

    polynomial = polynomial[:-3]
    return polynomial


def doubleNANDFunctionToStr(func, forceX):
    doubleNand = ""
    coeffs = func.doubleNAND_coeffs
    if forceX:
        variable = "x"
    else:
        variable = func.variable

    if func.functype == FuncTypes.SINUSOIDAL:
        for index in coeffs:
            if not coeffs.keys().__contains__(0):
                if index % 2 == 0:  # even exponents
                    if index == list(coeffs.keys())[0]:  # outermost
                        doubleNand = doubleNand + variable + "^2*(1-" + str(round(coeffs[index], 4))
                    elif index == list(coeffs.keys())[-1]:  # innermost
                        doubleNand = doubleNand + "*(1-" + str(round(coeffs[index], 4)) + "*" + variable + "^2"
                    else:  # inner
                        doubleNand = doubleNand + "*(1-" + variable + "^2*(1-" + str(round(coeffs[index], 4))
                else:  # odd exponents
                    print("TODO FEATURE ERROR!!!")
    else:
        for index in coeffs:
            if index == list(coeffs.keys())[0]:  # outermost
                doubleNand = doubleNand + "1-" + str(round(coeffs[index], 4)) + "*("
            else:
                if index == list(coeffs.keys())[-1]:  # innermost
                    doubleNand = doubleNand + "1-" + str(round(coeffs[index], 4)) + "*" + variable
                else:  # inner
                    doubleNand = doubleNand + "1-" + variable + "*(1-" + str(round(coeffs[index], 4)) + "*("

    doubleNand = doubleNand + ")" * (doubleNand.count("("))
    return doubleNand


def hornerFunctionToStr(func, forceX):
    horner = ""
    coeffs = func.horner_coeffs
    if forceX:
        variable = "x"
    else:
        variable = func.variable

    if func.functype == FuncTypes.SINUSOIDAL:
        for index in coeffs:
            if index == 0:  # cos
                if 0.998 <= float(round(coeffs[index], 4)) <= 1.001:
                    continue
                horner = horner + str(round(coeffs[index], 4)) + "*("
            if index == 1:  # sin
                if 0.998 <= float(round(coeffs[index], 4)) <= 1.001:
                    horner = horner + variable + "*("
                    continue
                horner = horner + str(round(coeffs[index], 4)) + " * " + variable + "*("
            else:
                if 0.998 <= float(round(coeffs[index], 4)) <= 1.001:
                    horner = horner + "1-" + variable + "^2"
                else:
                    horner = horner + "1-" + str(round(coeffs[index], 4)) + "*" + variable + "^2"

                if list(coeffs.keys())[(len(coeffs) - 1)] != index:  # not last coeff, series continues
                    horner = horner + "*("
    else:
        for index in coeffs:
            if index == 0:
                if 0.998 <= float(round(coeffs[index], 4)) <= 1.001:
                    continue
                else:
                    horner = horner + str(round(coeffs[index], 4)) + "*("
            if index == 1:
                if horner == "":
                    horner = horner + str(round(coeffs[index], 4)) + "*" + variable + "*("
                else:
                    if 0.998 <= float(round(coeffs[index], 4)) <= 1.001:
                        horner = horner + "1-" + variable
                    else:
                        horner = horner + "1-" + str(round(coeffs[index], 4)) + "*" + variable

                    if list(coeffs.keys())[(len(coeffs) - 1)] != index:  # not last coeff, series continues
                        horner = horner + "*("
            if index != 1 and index != 0:
                if 0.998 <= float(round(coeffs[index], 4)) <= 1.001:
                    horner = horner + "1-" + variable
                else:
                    horner = horner + "1-" + str(round(coeffs[index], 4)) + "*" + variable

                if list(coeffs.keys())[(len(coeffs) - 1)] != index:  # not last coeff, series continues
                    horner = horner + "*("

    horner = horner + ")" * (horner.count("("))
    return horner


def make_taylor_coeffs(func):
    coeffs = {}
    for n in range(func.order):
        order = (n + 1) if n % 2 == 0 else (n + 2)
        if func.isSinusoidal():
            coeffs[n] = derivative(func.function, func.point, n=n, order=order, dx=1e-2) / factorial(n)
        else:
            coeffs[n] = derivative(func.function, func.point, n=n, order=order, dx=1e-3) / factorial(n)
    return coeffs


def expand_binomial(point, n):
    coeffs = dict()
    for k in range(n + 1):
        coeff = ((-1) ** k) * comb(n, k) * (point ** k)
        coeffs[n - k] = coeff
    return coeffs


def make_polynomial(func):
    if func.point == 0:
        return func.taylor_coeffs
    else:
        new_taylor_coeffs = []
        final_dict = defaultdict(list)
        for power, coeff in func.taylor_coeffs.items():
            temp_dict = expand_binomial(func.point, power)
            temp_dict.update((x, y * coeff) for x, y in temp_dict.items())
            new_taylor_coeffs.append(temp_dict)
        for d in new_taylor_coeffs:
            for key, value in d.items():
                final_dict[key].append(value)
        final_dict.update((x, sum(y)) for x, y in final_dict.items())
        return dict(final_dict)


def ignore_small_coeffs(coeffs, ignore_th=1e-4):
    coeffs_new = {}
    for index in coeffs:
        if abs(coeffs[index]) > ignore_th:
            coeffs_new[index] = coeffs[index]
    return coeffs_new


def make_horner(func):
    func.horner_coeffs = ignore_small_coeffs(func.poli_coeffs)
    horner_coeffs = {}

    prev_index = 0
    for counter, index in enumerate(func.horner_coeffs):
        if counter == 0:
            horner_coeffs[index] = func.horner_coeffs[index]
        else:
            horner_coeffs[index] = -func.horner_coeffs[index] / func.horner_coeffs[prev_index]
        prev_index = index
    return horner_coeffs


def make_doubleNAND(func):
    func.doubleNAND_coeffs = ignore_small_coeffs(func.poli_coeffs)
    coeffs = {}
    tempList = list(func.doubleNAND_coeffs.values())
    tempListKeys = list(func.doubleNAND_coeffs.keys())

    for index in func.doubleNAND_coeffs:
        if index == 0:  # first coeff
            coeffs[index] = (1 - func.doubleNAND_coeffs[index])
        if index == tempListKeys[-1]:  # last in coeffs
            total = 0
            for indexj in func.doubleNAND_coeffs:
                total = total + func.doubleNAND_coeffs[indexj]
            total = total - tempList[-1]
            coeffs[index] = (func.doubleNAND_coeffs[index]) / (1 - total)
        else:
            total = 0
            for indexj in func.doubleNAND_coeffs:
                if index > indexj:
                    total = total + func.doubleNAND_coeffs[indexj]
            coeffs[index] = (1 - (total + func.doubleNAND_coeffs[index])) / (1 - total)
    return coeffs


def AddBaseGate(graph, gateIndex, gateType, val1Type, value1, val2Type, value2):
    assert gateType in [GateTypes.NAND.value,
                        GateTypes.BNAND.value,
                        GateTypes.AND.value,
                        GateTypes.BAND.value,
                        GateTypes.MUX.value]

    # add check to ignore unnecessary AND gate
    # if ((gateType == GateTypes.AND.value and (value1 <= 1+1e-4 and value1 >= 1-1e-4)
    #    or gateType == GateTypes.AND.value and (value2 <= 1+1e-4 and value2 >= 1-1e-4)) and gateIndex != 1):
    #    gateIndex = gateIndex - 1
    #    return graph

    if type(value1) is not str:
        graph.add_edge((val1Type, str(round(value1, 4))),
                       (gateType, "G" + str(gateIndex)))
    else:
        graph.add_edge((val1Type, value1),
                       (gateType, "G" + str(gateIndex)))

    if type(value2) is not str:
        graph.add_edge((val2Type, str(round(value2, 4))),
                       (gateType, "G" + str(gateIndex)))
    else:
        graph.add_edge((val2Type, value2),
                       (gateType, "G" + str(gateIndex)))

    return graph


def AddGateFromGate(graph, prevGateType, prevGateIndex, newGateIndex, gateType, valType, value):
    assert gateType in [GateTypes.NAND.value,
                        GateTypes.BNAND.value,
                        GateTypes.AND.value,
                        GateTypes.BAND.value,
                        GateTypes.MUX.value]

    # add check to ignore unnecessary AND gate
    # if (valType == NotGateTypes.CONSTANT.value):
    #    if (gateType == GateTypes.AND.value and (float(value) <= 1.0001 and float(value) >= 0.9998)):
    #        newGateIndex = newGateIndex - 1
    #        return graph
    # else:
    graph.add_edge((prevGateType, "G" + str(prevGateIndex)),
                   (gateType, "G" + str(newGateIndex)))
    if type(value) is not str:
        graph.add_edge((valType, str(round(value, 4))),
                       (gateType, "G" + str(newGateIndex)))
    else:
        graph.add_edge((valType, value),
                       (gateType, "G" + str(newGateIndex)))

    return graph


def doubleNAND_to_circuit(func):
    graph = nx.DiGraph()
    gateIndex = 1

    # Ways to create a gate:
    #           AddBaseGate(graph, gateIndex, gateType, val1Type, value1, val2Type, value2)
    #           AddGateFromGate(graph, prevGateType, prevGateIndex, newGateIndex, gateType, valType, value)
    #

    if func.isSinusoidal():  # uses x^2
        coeffs = dict(reversed(list(func.doubleNAND_coeffs.items())))
        xSquaredGate = 0
        for index in coeffs:
            if index == list(coeffs.keys())[0]:  # innermost
                # AND x with itself (x^2)
                AddBaseGate(graph, gateIndex, GateTypes.AND.value,  # graph, GIndex, GateType
                            NotGateTypes.INPUT.value, func.variable.upper(),  # Value1 Type, Value1
                            NotGateTypes.INPUT.value, func.variable.upper() + " ")  # Value2 Type, Value2
                xSquaredGate = gateIndex
                gateIndex = gateIndex + 1

                # NAND prev result with coeff
                AddGateFromGate(graph, GateTypes.AND.value, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                gateIndex = gateIndex + 1
            else:
                if index == list(coeffs.keys())[-1]:  # outermost
                    # NAND prev result with coeff
                    AddGateFromGate(graph, GateTypes.NAND.value, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                    NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                    gateIndex = gateIndex + 1

                    # AND prev result with x^2, finish
                    AddGateFromGate(graph, GateTypes.AND.value, xSquaredGate,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                    GateTypes.NAND.value, "G" + str(gateIndex - 1))  # valType, value
                else:  # inner (minus innermost)
                    # NAND prev result with coeff
                    AddGateFromGate(graph, GateTypes.NAND.value, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                    NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                    gateIndex = gateIndex + 1

                    # NAND pev result with x^2
                    AddGateFromGate(graph, GateTypes.AND.value, xSquaredGate,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                    GateTypes.NAND.value, "G" + str(gateIndex - 1))  # valType, value
                    gateIndex = gateIndex + 1
    else:  # only uses x
        coeffs = dict(reversed(list(func.doubleNAND_coeffs.items())))
        print(coeffs)

        for index in coeffs:
            if index == 0:  # outermost
                # NAND coeff i==n with prev result, finish
                AddGateFromGate(graph, GateTypes.NAND.value, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
            else:
                if list(coeffs.keys())[0] == index:  # innermost
                    # NAND coeff i==0 with x
                    AddBaseGate(graph, gateIndex, GateTypes.NAND.value,  # graph, GIndex, GateType
                                NotGateTypes.INPUT.value, func.variable.upper(),  # Value1 Type, Value1
                                NotGateTypes.CONSTANT.value, coeffs[index])  # Value2 Type, Value2
                    gateIndex = gateIndex + 1
                else:  # middle section
                    # NAND coeff with prev result
                    AddGateFromGate(graph, GateTypes.NAND.value, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                    NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                    gateIndex = gateIndex + 1

                    # NAND x with prev result
                    AddGateFromGate(graph, GateTypes.NAND.value, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                    NotGateTypes.INPUT.value, func.variable.upper())  # valType, value
                    gateIndex = gateIndex + 1
    gate_nodes = []

    for node in graph.nodes():
        if GateTypes.isIn(node[0]):
            gate_nodes.append(node)

    if gate_nodes[(len(gate_nodes) - 1)][0] == GateTypes.AND.value:
        graph.add_edge((GateTypes.AND.value, "G" + str(len(gate_nodes))),
                       (NotGateTypes.OUTPUT.value, "f(" + func.variable + ")"))

    elif gate_nodes[(len(gate_nodes) - 1)][0] == GateTypes.NAND.value:
        graph.add_edge((GateTypes.NAND.value, "G" + str(len(gate_nodes))),
                       (NotGateTypes.OUTPUT.value, "f(" + func.variable + ")"))

    for node in gate_nodes:
        print(node[0] + " - " + node[1])
        print(list(graph.predecessors(node)))
        print("=" * 100)
    return graph


def horner_to_circuit(func):
    graph = nx.DiGraph()
    gateIndex = 1
    previousGate = ""
    coeffs = func.horner_coeffs

    transCoeffs = reversed(coeffs)

    # Ways to create a gate:
    #           AddBaseGate(graph, gateIndex, gateType, val1Type, value1, val2Type, value2)
    #           AddGateFromGate(graph, prevGateType, prevGateIndex, newGateIndex, gateType, valType, value)
    #

    if func.isSinusoidal():  # only uses x^2
        numX = 1
        xSquaredGate = 0
        for index in transCoeffs:
            if list(coeffs.keys())[(len(coeffs) - 1)] == index:  # First grouping (innermost 1-jx^2, where j is coeff)
                # AND x with itself (x^2)
                AddBaseGate(graph, gateIndex, GateTypes.AND.value,  # graph, GIndex, GateType
                            NotGateTypes.INPUT.value, func.variable.upper(),  # Value1 Type, Value1
                            NotGateTypes.INPUT.value, func.variable.upper() + " ")  # Value2 Type, Value2
                xSquaredGate = gateIndex
                gateIndex = gateIndex + 1
                previousGate = GateTypes.AND.value

                # NAND prev result with next coeff last coefficient
                AddGateFromGate(graph, previousGate, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                gateIndex = gateIndex + 1
                previousGate = GateTypes.NAND.value

            else:
                if index != 1 and index != 0:  # In between groupings (next few 1-jx^2, where j is coeff)
                    # AND prev result (gIndex - 2) with x^2 value (xSquaredGate yields index)
                    AddGateFromGate(graph, previousGate, xSquaredGate,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                    GateTypes.NAND.value, "G" + str(gateIndex - 1))  # valType, value
                    gateIndex = gateIndex + 1
                    previousGate = GateTypes.AND.value

                    # NAND prev result with next coeff
                    AddGateFromGate(graph, previousGate, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                    NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                    gateIndex = gateIndex + 1
                    previousGate = GateTypes.NAND.value

                else:  # last grouping where case 1: jx(1-kx^2(...)) is last group (i == 1), or case 2: 1-jx^2(...)
                    # is last group (i == 0)
                    if index == 1:  # case 1, last term, sin(x)
                        # AND prev result with X
                        AddGateFromGate(graph, previousGate, gateIndex - 1, # graph, prevGateType, prevGateIndex
                                        gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                        NotGateTypes.INPUT.value, func.variable.upper())  # valType, value
                        gateIndex = gateIndex + 1
                        previousGate = GateTypes.AND.value

                        # AND prev result with first coeff
                        if not FrivelousNumber(coeffs[index]):
                            AddGateFromGate(graph, previousGate, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                            gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                            NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                            gateIndex = gateIndex + 1
                            previousGate = GateTypes.AND.value

                    else:  # case 2, index == 0, last term, cos(x)
                        # AND prev result with first coeff
                        if not FrivelousNumber(coeffs[index]):
                            AddGateFromGate(graph, previousGate, gateIndex - 1, # graph, prevGateType, prevGateIndex
                                            gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                            NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                            gateIndex = gateIndex + 1
                            previousGate = GateTypes.AND.value

    else:  # only uses x^1
        for index in transCoeffs:
            if list(coeffs.keys())[(len(coeffs) - 1)] == index:  # First grouping (innermost 1-jx, where j is coeff)
                # NAND X and last coeff
                AddBaseGate(graph, gateIndex, GateTypes.NAND.value,  # graph, GIndex, GateType
                            NotGateTypes.INPUT.value, func.variable.upper(),  # Value1 Type, Value1
                            NotGateTypes.CONSTANT.value, coeffs[index])  # Value2 Type, Value2
                gateIndex = gateIndex + 1
                previousGate = GateTypes.NAND.value

            else:
                if index != 1 and index != 0:  # In between groupings (next few 1-jx, where j is coeff)
                    if not FrivelousNumber(coeffs[index]):
                        # AND prev result with next coeff
                        AddGateFromGate(graph, previousGate, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                        gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                        NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                        gateIndex = gateIndex + 1
                        previousGate = GateTypes.AND.value

                    # NAND prev result with X
                    AddGateFromGate(graph, previousGate, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                    gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                    NotGateTypes.INPUT.value, func.variable.upper())  # valType, value
                    gateIndex = gateIndex + 1
                    previousGate = GateTypes.NAND.value

                else:  # Last grouping, where case 1: jx(...) is last group (i == 1), or case 2: j(1-kx(...)) is last
                    # group (i == 1)
                    if 0 not in list(coeffs.keys()):  # case 1 - jx(...)
                        if not FrivelousNumber(coeffs[index]):
                            # AND prev result with next coeff
                            AddGateFromGate(graph, previousGate, gateIndex - 1,
                                            # graph, prevGateType, prevGateIndex
                                            gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                            NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                            gateIndex = gateIndex + 1
                            previousGate = GateTypes.AND.value

                        # AND prev output with X
                        AddGateFromGate(graph, previousGate, gateIndex - 1,  # graph, prevGateType, prevGateIndex
                                        gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                        NotGateTypes.INPUT.value, func.variable.upper())  # valType, value
                        previousGate = GateTypes.AND.value

                    else:  # case 2 - j(1-kx(...))
                        if index == 1:
                            if not FrivelousNumber(coeffs[index]):
                                # AND prev result with next coeff
                                AddGateFromGate(graph, previousGate, gateIndex - 1,
                                                # graph, prevGateType, prevGateIndex
                                                gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                                NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                                gateIndex = gateIndex + 1
                                previousGate = GateTypes.AND.value

                            # NAND prev result with X
                            AddGateFromGate(graph, previousGate, gateIndex - 1,
                                            # graph, prevGateType, prevGateIndex
                                            gateIndex, GateTypes.NAND.value,  # newGateIndex, gateType
                                            NotGateTypes.INPUT.value, func.variable.upper())  # valType, value
                            gateIndex = gateIndex + 1
                            previousGate = GateTypes.NAND.value

                        else:  # index == 0
                            if not FrivelousNumber(coeffs[index]):
                                # AND prev result with next coeff
                                AddGateFromGate(graph, previousGate, gateIndex - 1,
                                                # graph, prevGateType, prevGateIndex
                                                gateIndex, GateTypes.AND.value,  # newGateIndex, gateType
                                                NotGateTypes.CONSTANT.value, coeffs[index])  # valType, value
                                gateIndex = gateIndex + 1
                                previousGate = GateTypes.AND.value

    gate_nodes = []

    for node in graph.nodes():
        if GateTypes.isIn(node[0]):
            gate_nodes.append(node)

    if gate_nodes[(len(gate_nodes) - 1)][0] == GateTypes.AND.value:
        graph.add_edge((GateTypes.AND.value, "G" + str(len(gate_nodes))),
                       (NotGateTypes.OUTPUT.value, "f(" + func.variable + ")"))

    elif gate_nodes[(len(gate_nodes) - 1)][0] == GateTypes.NAND.value:
        graph.add_edge((GateTypes.NAND.value, "G" + str(len(gate_nodes))),
                       (NotGateTypes.OUTPUT.value, "f(" + func.variable + ")"))

    for node in gate_nodes:
        print(node[0] + " - " + node[1])
        print(list(graph.predecessors(node)))
        print("=" * 100)

    return graph


def FrivelousNumber(number):
    if 0.998 <= number <= 1.001:
        return True
    else:
        return False


def show_graph(func):
    graph = func.circuit
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(graph)

    color_map = []
    temp = 0
    for node in graph.nodes():

        if GateTypes.isIn(node[0]):
            color_map.append("orange")
            temp = 1

        if NotGateTypes.isIn(node[0]):
            color_map.append("yellow")
            temp = 1

        if temp == 0:
            color_map.append("red")
        else:
            temp = 0

    plt.title(func.title)

    nx.draw_networkx_nodes(graph, pos, node_color=color_map)
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color='b', arrows=True)

    plt.savefig("assets/result.png", format="PNG")

    plt.show()


def make_reactions(graph):
    reactionStr = ""
    for node in graph:
        if GateTypes.isIn(node[0]):
            gate_type = node[0]
            input_substances = list(graph.predecessors(node))
            output_substances = list(graph.neighbors(node))
            gateName = node[1]

            reactionStr = reactionStr + gateName + "(" + gate_type + ")\n" \
                          + "Inputs: " + input_substances[0][1] + ", " + input_substances[1][1] + "\n" \
                          + "Output(s) To: "

            for output in output_substances:
                reactionStr = reactionStr + " " + output[1]

            reactionStr = reactionStr + "\n\nReaction Table:\n"

            reaction = make_reaction(gate_type, input_substances, output_substances, gateName)

            for r in reaction:
                print(r)
                reactionStr = reactionStr + r + "\n"
            print("-" * 100)

            reactionStr = reactionStr + "-" * 85 + "\n"

    return reactionStr


def make_reaction(gate_type, input_substances, output_substances, gateName):
    assert gate_type in [GateTypes.NAND.value,
                         GateTypes.BNAND.value,
                         GateTypes.AND.value,
                         GateTypes.BAND.value,
                         GateTypes.MUX.value]

    assert len(input_substances) == 2

    print(gate_type, "(", gateName, ")")
    print(input_substances)
    print(output_substances)

    a = input_substances[0][1]
    b = input_substances[1][1]
    c = gateName

    if gate_type == GateTypes.AND.value:
        reaction_list = [
            f"{a}_0 + {b}_0 -> {c}_0",
            f"{a}_0 + {b}_1 -> {c}_0",
            f"{a}_1 + {b}_0 -> {c}_0",
            f"{a}_1 + {b}_1 -> {c}_1",
        ]
    elif gate_type == GateTypes.NAND.value:
        reaction_list = [
            f"{a}_0 + {b}_0 -> {c}_1",
            f"{a}_0 + {b}_1 -> {c}_1",
            f"{a}_1 + {b}_0 -> {c}_1",
            f"{a}_1 + {b}_1 -> {c}_0",
        ]
    else:
        print("GATE ERROR: Given Gate Type ", gate_type)
        return -1
    return reaction_list
