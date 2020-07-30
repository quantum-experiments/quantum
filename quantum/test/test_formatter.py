import numpy as np
from quantum.formatter import pprint_fraction

def test_pprint():
    assert pprint_fraction(0.3333333333) == "1/3"
    assert pprint_fraction(0.25) == "1/4"
    assert pprint_fraction(1/np.sqrt(2)) == "1/√2"
    assert pprint_fraction(-1/np.sqrt(2)) == "-1/√2"
