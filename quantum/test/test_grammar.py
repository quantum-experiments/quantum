from quantum.grammar import grammar, QuantumVisitor

def test_grammar1():
    text = "H(0)"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed == {
        "gates": [
            {
                "gate": "H",
                "args": ["0"]
            }
        ],
        "qubits": None
    }

def test_grammar2():
    text = "|00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed == {
        "gates": None,
        "qubits": "00"
    }

def test_grammar3():
    text = "H(0) |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed == {
        "gates": [
            {
                "gate": "H",
                "args": ["0"]
            }
        ],
        "qubits": "00"
    }

def test_grammar4():
    text = "H(0).CX(01) |00>"
    parsed = QuantumVisitor().visit(grammar.parse(text))
    assert parsed == {
        "gates": [
            {
                "gate": "H",
                "args": ["0"]
            },
            {
                "gate": "CX",
                "args": ["01"]
            }
        ],
        "qubits": "00"
    }
