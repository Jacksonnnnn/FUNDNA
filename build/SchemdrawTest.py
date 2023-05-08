import schemdraw
from schemdraw import logic
from schemdraw.parsing import logicparse

# with logicparse('(a and b) and (y nand x)', outlabel='$f(x)$') as d:
#    d.save('my_circuit.svg')

# with schemdraw.Drawing() as d:
#      d += (a := logic.And().label('b', 'in1'))
#      d += (b := logic.Or().at(a.out, dy=-.5).anchor('in1').label('f', 'out'))
#      d += logic.Line().at(a.out).to(b.in1)
#      d += logic.Line().at(a.in2).toy(b.in2)
#      d += logic.Line().at(b.in2).tox(a.in2.x-.5).label('a', 'left')

# logic gate drawing of (x^2)/10 + x/15 + 4/5
with schemdraw.Drawing() as d:
    d += (g1 := logic.Nand().label('0.75', 'in1').label('X', 'in2'))
    d += g1.label('G1', 'center')
    d += (g2 := logic.Nand().at(g1.out).anchor('in2').label('0.6667', 'in1', ofst=(0, 0.5)))
    d += g2.label('G2', 'center')
    d += (g3 := logic.Nand().at(g2.out).anchor('in1'))
    d += g3.label('G3', 'center')
    d += (g4 := logic.Nand().at(g3.out).anchor('in2').label('0.2', 'in1', ofst=(0, 0.5)).label('$f(x)$', 'out'))
    d += g4.label('G4', 'center')
    d += logic.Wire('n', k=-0.5).at(g1.in2).to(g3.in2)

d.draw()
d.save('my_circuit.svg')

def AddBaseGate(drawing, gateIndex, gateType, val1Type, value1, val2Type, value2):
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


def AddGateFromGate(drawing, prevGateType, prevGateIndex, newGateIndex, gateType, valType, value):
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
