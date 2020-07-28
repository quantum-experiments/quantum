import numpy as np

from quantum.grammar import parse
from quantum.calculate import *
from quantum.states import one, zero

text = "H(0)"
text = "|00>"
text = "H(0) |00>"
text = "CX(01).H(0) |00>"
text = "H(0).X(1) |00>"
text = "|-+>"

def test_calculate():
    text = "X(0) |00>"
    assert evaluate(parse(text)) == np.kron(one, zero)
