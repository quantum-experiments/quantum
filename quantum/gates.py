import numpy as np

def _gate(*values):
    return np.array(values)

I = _gate((1, 0), (0, 1))
H = _gate((1,1), (1,-1))
X = _gate((0, 1), (1, 0))
Y = _gate((0, 1j), (1j, 0))
Z = _gate((1, 0), (0, -1))
P0 = np.kron(_gate(1, 0), _gate(0, 1).T)
P1 = np.kron(_gate(0, 1), _gate(1, 0).T)
CNOT01 = np.kron(P0, I) + np.kron(P1, X)
