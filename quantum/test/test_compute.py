import pytest
import numpy as np

from quantum.compute import evaluate
from quantum.states import one, zero, plus, minus, _norm

@pytest.mark.parametrize("text, state", [
    ("X0 |00>", np.kron(one, zero)),
    ("H0 |0>", plus),
    ("|00>", np.kron(zero, zero)),
    ("H0 |00>", np.kron(plus, zero)),
    ("CX01 H0 |00>", _norm(np.kron(zero, zero) + np.kron(one, one))),
    ("H0.X1 |00>", np.kron(plus, one)),
    ("|-+>", np.kron(minus, plus)),
])
def test_compute(text, state):
    assert np.all(evaluate(text) == state)
