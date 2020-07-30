from quantum.grammar import grammar, QuantumVisitor

def test_grammar1():
    text = "H0"
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
    text = "H0 |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    (gate,) = parsed.gates[0]
    assert gate.name == "H"
    assert gate.args == ("0", )
    assert parsed.target.bitstring == "00"

def test_grammar4():
    text = "CX01 H0 |00>"
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
    text = "CX01 X1 H0.X1 |00>"
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

def test_grammar7():
    text = "FOO |0>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    gate, = parsed.gates[0]
    assert gate.name == "FOO"
    assert gate.args == ()
    assert parsed.target.bitstring == "0"
