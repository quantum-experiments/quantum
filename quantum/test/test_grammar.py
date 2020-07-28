from quantum.grammar import grammar, QuantumVisitor

def test_grammar1():
    text = "H(0)"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].gate == "H"
    assert parsed.gates[0].args == ["0"]
    assert parsed.qubits is None

def test_grammar2():
    text = "|00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates == None
    assert parsed.qubits == "00"

def test_grammar3():
    text = "H(0) |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].gate == "H"
    assert parsed.gates[0].args == ["0"]
    assert parsed.qubits == "00"

def test_grammar4():
    text = "H(0).CX(01) |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed.gates[0].gate == "H"
    assert parsed.gates[0].args == ["0"]
    assert parsed.gates[1].gate == "CX"
    assert parsed.gates[1].args == ["01"]
    assert parsed.qubits == "00"
