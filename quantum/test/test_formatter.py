import numpy as np
from quantum.formatter.fraction import pprint_fraction

def test_pprint():
    assert pprint_fraction(0.3333333333) == "1/3"
    assert pprint_fraction(0.25) == "1/4"
    assert pprint_fraction(1/np.sqrt(2)) == "1/√2"
    assert pprint_fraction(-1/np.sqrt(2)) == "-1/√2"
    assert pprint_fraction(1j/np.sqrt(2)) == "i/√2"
    assert pprint_fraction(500j/409) == "500i/409"
    assert pprint_fraction(1j) == "i"
