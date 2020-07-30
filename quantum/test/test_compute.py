import numpy as np

from quantum.compute import evaluate
from quantum.states import one, zero

text = "H0"
text = "|00>"
text = "H0 |00>"
text = "CX01 H0 |00>"
text = "H0.X1 |00>"
text = "|-+>"

def test_compute():
    text = "X0 |00>"
    assert np.all(evaluate(text) == np.kron(one, zero))
