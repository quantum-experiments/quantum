from quantum.grammar import grammar, QuantumVisitor

def test_grammar1():
    text = "H(0)"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].name == "H"
    assert parsed.gates[0].args == ("0", )
    assert parsed.qubits is None

def test_grammar2():
    text = "|00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates == None
    assert parsed.qubits == "00"

def test_grammar3():
    text = "H(0) |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].name == "H"
    assert parsed.gates[0].args == ("0", )
    assert parsed.qubits == "00"

def test_grammar4():
    text = "CX(01).H(0) |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[1].name == "H"
    assert parsed.gates[1].args == ("0", )
    assert parsed.gates[0].name == "CX"
    assert parsed.gates[0].args == ("01", )
    assert parsed.qubits == "00"

def test_grammar5():
    text = "|-+>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates == None
    assert parsed.qubits == "-+"