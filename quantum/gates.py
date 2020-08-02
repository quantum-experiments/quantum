import numpy as np

from quantum.formatter.fraction import farray
from quantum.states import one, zero


def _gate(*values):
    return np.array(values).view(farray)

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
CNOT10 = np.kron(I, P0) + np.kron(X, P1)
CNOT12 = np.kron(I, CNOT01)
CNOT21 = np.kron(I, CNOT10)
CNOT012 = np.kron(CNOT01,I)
CNOT102 = np.kron(CNOT10,I)
T = np.array([[1, 0], [0, np.exp(1j*np.pi/4)]])
TD = np.conjugate(T)

name_gates = {
    "I": I,
    "H": H,
    "X": X,
    "Y": Y,
    "Z": Z,
    "T": T,
    "TD": TD,
    "CNOT01": CNOT01,
    "CNOT10": CNOT10,
    "CNOT012": CNOT012,
    "CNOT102": CNOT102,
    "CNOT12": CNOT12,
    "CNOT21": CNOT21,
}

def add_gate(label: str, value: np.ndarray, overwrite: bool = False):
    if label not in name_gates or overwrite:
        name_gates[label] = value
    else:
        raise ValueError("Gate {label} already exists.")
