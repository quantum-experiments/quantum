from quantum.grammar import grammar, QuantumVisitor

def test_grammar1():
    text = "H[0]"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].name == "H"
    assert parsed.gates[0].args == ("0", )
    assert parsed.target is None

def test_grammar2():
    text = "|00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates == None
    assert parsed.target.bitstring == "00"

def test_grammar3():
    text = "H[0] |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].name == "H"
    assert parsed.gates[0].args == ("0", )
    assert parsed.target.bitstring == "00"

def test_grammar4():
    text = "CX[01] H[0] |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].name == "CX"
    assert parsed.gates[0].args == ("01", )
    target = parsed.target
    assert target.gates[0].name == "H"
    assert target.gates[0].args == ("0", )
    assert target.target.bitstring == "00"

def test_grammar5():
    text = "CX[01] X[1] H[0].X[1] |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].name == "CX"
    assert parsed.gates[0].args == ("01", )
    target = parsed.target
    assert target.gates[0].name == "X"
    assert target.gates[0].args == ("1", )
    target = target.target
    assert target.gates[0].name == "H"
    assert target.gates[0].args == ("0", )
    assert target.target.bitstring == "00"

def test_grammar6():
    text = "|-+>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates == None
    assert parsed.target.bitstring == "-+"