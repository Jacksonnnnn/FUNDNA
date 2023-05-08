import schemdraw
from schemdraw import logic
from schemdraw.parsing import logicparse
from Gate import Gate

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
    d += logic.Wire('n', k=-0.5).at(g1.out).to(g3.in2)
    d += g4.label('fuck you', 'out')

d.draw()
d.save('my_circuit.svg')

for elem in d.elements:
    if type(elem) is schemdraw.logic.logic.And or type(elem) is schemdraw.logic.logic.Nand:
        print('-' * 15)
        print(elem)
        print(elem.segments)
        print(elem.__str__())

#  Gate() : gateType, input1, input1Type, input2, input2Type, output, outputType, index, isBase, isXsquared


def AddBaseGate(drawing, gateIndex, gateType, in1, in1Type, in2, in2Type, isXsquared):
    assert type(drawing) == schemdraw.Drawing()
    gateWrapper = Gate(gateType, in1, in1Type, in2, in2Type, out, outType, gateIndex, True, isXsquared)

    if in1 is not str:
        if in1 is float:
            in1 = round(in1, 4)

        in1 = str(in1)

    if in2 is not str:
        if in2 is float:
            in2 = round(in2, 4)

        in2 = str(in2)

    with drawing as d:
        if gateType == GateTypes.NAND:
            d += (gate := logic.Nand().label(in1, 'in1').label(in2, 'in2'))
            d += gate.label("G" + str(gateIndex), 'center')
        if gateType == GateTypes.AND:
            d += (gate := logic.And().label(in1, 'in1').label(in2, 'in2'))
            d += gate.label("G" + str(gateIndex), 'center')

    gateWrapper.gate = gate

    return d, gateWrapper


def AddGateFromGate(drawing, prevGate, baseGate, gateType, gateIndex, inValue, inType, out, outType, connectBase):
    assert type(drawing) == schemdraw.Drawing()
    assert type(prevGate) == schemdraw.logic.logic
    gateWrapper = Gate(gateType, None, None, inValue, inType, out, outType, gateIndex, False, False)

    if inValue is not str:
        if inValue is float:
            inValue = round(inValue, 4)

        inValue = str(inValue)

    with drawing as d:
        if not connectBase:
            if gateType == GateTypes.NAND:
                d += (gate := logic.Nand().at(prevGate.out).anchor('in2').label(inValue, 'in1', ofst=(0, 0.5)))
                d += gate.label("G" + str(gateIndex), 'center')
            if gateType == GateTypes.AND:
                d += (gate := logic.And().at(prevGate.out).anchor('in2').label(inValue, 'in1', ofst=(0, 0.5)))
                d += gate.label("G" + str(gateIndex), 'center')
        else:
            if gateType == GateTypes.NAND:
                d += (gate := logic.Nand().at(prevGate.out).anchor('in1'))
                d += gate.label("G" + str(gateIndex), 'center')
            if gateType == GateTypes.AND:
                d += (gate := logic.And().at(prevGate.out).anchor('in1'))
                d += gate.label("G" + str(gateIndex), 'center')

            d += logic.Wire('n', k=-0.5).at(baseGate.in2).to(gate.in2)

    gateWrapper.gate = gate

    return drawing, gateWrapper
