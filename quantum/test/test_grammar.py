import pytest

from quantum.grammar import parse

@pytest.mark.parametrize("text, pprint_value", [
    ("H0", "H₀"),
    ("|00>", "|00⟩"),
    ("H0 |00>", "H₀  |00⟩"),
    ("CX01 H0 |00>", "CX₀,₁  H₀  |00⟩"),
    ("CX11,12 H0 |00>", "CX₁₁,₁₂  H₀  |00⟩"),
    ("CX01 X1 H0*X1 |00>", "CX₀,₁  X₁  H₀ ⨂ X₁  |00⟩"),
    ("|-+>", "|-+⟩"),
    ("FOO |0>", "FOO  |0⟩"),
    ("X0 X0 H0 X0", "X₀  X₀  H₀  X₀"),
])
def test_compute(text, pprint_value):
    assert str(parse(text)) == pprint_value
