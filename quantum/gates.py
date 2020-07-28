import numpy as np
from quantum.states import zero, one

def _gate(*values):
    return np.array(values)

def _norm(gate):
    return gate / np.linalg.norm(gate, axis = 1, keepdims = True)

I = _gate((1, 0), (0, 1))
H = _norm(_gate((1,1), (1,-1)))
X = _gate((0, 1), (1, 0))
Y = _gate((0, 1j), (1j, 0))
Z = _gate((1, 0), (0, -1))
P0 = np.kron(zero, zero.T)
P1 = np.kron(one, one.T)
CNOT01 = np.kron(P0, I) + np.kron(P1, X)
