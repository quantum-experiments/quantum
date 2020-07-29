from quantum.grammar import grammar, QuantumVisitor

def test_grammar1():
    text = "H[0]"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    (gate,) = parsed.gates[0]
    assert gate.name == "H"
    assert gate.args == ("0", )
    assert parsed.target is None

def test_grammar2():
    text = "|00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates == None
    assert parsed.target.bitstring == "00"

def test_grammar3():
    text = "H[0] |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    (gate,) = parsed.gates[0]
    assert gate.name == "H"
    assert gate.args == ("0", )
    assert parsed.target.bitstring == "00"

def test_grammar4():
    text = "CX[01] H[0] |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    (gate,) = parsed.gates[1]
    assert gate.name == "CX"
    assert gate.args == ("01", )
    target = parsed.target
    (gate,) = parsed.gates[0]
    assert gate.name == "H"
    assert gate.args == ("0", )
    assert target.bitstring == "00"

def test_grammar5():
    text = "CX[01] X[1] H[0].X[1] |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))

    (gate,) = parsed.gates[2]
    assert gate.name == "CX"
    assert gate.args == ("01", )

    (gate,) = parsed.gates[1]
    assert gate.name == "X"
    assert gate.args == ("1", )

    (gate0, gate1) = parsed.gates[0]
    assert gate0.name == "H"
    assert gate0.args == ("0", )
    assert gate1.name == "X"
    assert gate1.args == ("1", )
    assert parsed.target.bitstring == "00"

def test_grammar6():
    text = "|-+>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates == None
    assert parsed.target.bitstring == "-+"