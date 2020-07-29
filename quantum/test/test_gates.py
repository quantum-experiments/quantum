import numpy as np
from quantum.gates import H

def test_gates():
    assert (H == np.array([[1, 1], [1, -1]])/np.sqrt(2)).all()
