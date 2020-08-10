import numpy as np

from quantum.formatter.fraction import pprint_fraction, farray

def pprint_qubits(bitstring: str, latex: bool = False):
    if latex:
        return f"\\lvert{bitstring}\\rangle"
    return f"|{bitstring}⟩"

def _to_qbit(value: int, norm: float, num_qubits: int, latex: bool):
    bitstring = np.binary_repr(value, num_qubits)
    norm_repr = f"{pprint_fraction(norm, latex=latex)} " if norm != 1 else ""
    return f"{norm_repr}{pprint_qubits(bitstring, latex)}"

def pprint_dirac(state: np.ndarray, latex: bool = False):
    """ pretty print for dirac notation of states """
    length, width = np.shape(state)
    num_qubits = int(np.log2(length))
    assert width == 1, f"Array shape {(length, width)} not supported"
    return " + ".join(_to_qbit(val, norm, num_qubits, latex) for val, norm in enumerate(state.flatten()) if norm != 0)

class dirac(farray):
    """ ndarray but with pretty printing of fractions, sqrt values and dirac notation """
    def _is_1d_vector(self):
        shape = np.shape(self)
        if len(shape) == 2:
            _, width = shape
            if width == 1:
                return True
        return False

    def __repr__(self):
        if self._is_1d_vector():
            return str(self)
        return super(dirac, self).__repr__()

    def __str__(self):
        if self._is_1d_vector():
            return pprint_dirac(self)
        return super(dirac, self).__str__()
    
    def _repr_latex_(self):
        if self._is_1d_vector():
            return f"${pprint_dirac(self, latex=True)}$"
        return super(dirac, self)._repr_latex_()
