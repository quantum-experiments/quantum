import numpy as np

from quantum.formatter.dirac import dirac

def _state(*values):
    return np.array([values]).T.view(dirac)

def _norm(state):
    return state / np.linalg.norm(state)

zero = _state(1,0)
one = _state(0,1)
plus = _norm(_state(1,1))
minus = _norm(_state(1,-1))

bit_states = {
    "0": zero,
    "1": one,
    "+": plus,
    "-": minus,
}
