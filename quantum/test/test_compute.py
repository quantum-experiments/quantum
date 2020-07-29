import numpy as np

from quantum.compute import evaluate
from quantum.states import one, zero

text = "H(0)"
text = "|00>"
text = "H(0) |00>"
text = "CX(01).H(0) |00>"
text = "H(0).X(1) |00>"
text = "|-+>"

def test_compute():
    text = "X0 |00>"
    assert np.all(evaluate(text) == np.kron(one, zero))
