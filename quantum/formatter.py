import numpy as np
import fractions

def _fraction_formatter(value: float):
    """ pretty print fraction value"""
    as_fraction = fractions.Fraction(value).limit_denominator()
    return str(as_fraction)

def _sqrt_formatter(value: float):
    """ pretty print fraction value with sqrt symbol """
    fraction = fractions.Fraction(value**2).limit_denominator()
    def _to_str(nom):
        if nom != 1:
            return f"√{nom}"
        return str(nom)
    
    sign = "-" if np.sign(value) == -1 else ""
    return f"{sign}{_to_str(fraction.numerator)}/{_to_str(fraction.denominator)}"

def pprint_fraction(value: float, no_sqrt: bool = False):
    """
    Pretty print for fractional and/or sqrt float values.
    Returns the shortest representation (e.g. "1/√2" or "4.1").

    :value: float value
    :no_sqrt: flag for not including sqrt terms
    """
    if no_sqrt:
        return _fraction_formatter(value)

    return min(
        _fraction_formatter(value), 
        _sqrt_formatter(value), 
        str(value), 
        key=lambda x: len(x)
    )

def pretty_farray(no_sqrt: bool = False):
    """
    context manager for pretty printing arrays with fractions and sqrt terms

    :no_sqrt: flag for not including sqrt terms
    """
    if no_sqrt:
        return np.printoptions(formatter={'float': lambda x: pprint_fraction(x, no_sqrt)})
    return np.printoptions(formatter={'float': pprint_fraction})

class farray(np.ndarray):
    """ ndarray but with pretty printing of fractions and sqrt values """
    def __repr__(self):
        with pretty_farray():
            return super(farray, self).__repr__()

    def __str__(self):
        with pretty_farray():
            return super(farray, self).__str__()

def _to_qbit(value: int, norm: float, num_qubits: int):
    bin_repr = np.binary_repr(value, num_qubits)
    norm_repr = f"{pprint_fraction(norm)} " if norm != 1 else ""
    return f"{norm_repr}|{bin_repr}>"

def pretty_dirac(state: np.ndarray):
    """ pretty print for dirac notation of states """
    length, width = np.shape(state)
    num_qubits = int(np.log2(length))
    assert width == 1, f"Array shape {(length, width)} not supported"
    return " + ".join(_to_qbit(val, norm, num_qubits) for val, norm in enumerate(state.flatten()) if norm != 0)

def _to_subscript(args: tuple):
    args_str = ",".join(args)
    return "_{%s}" %args_str

def pretty_gate_sequence(gates: tuple):
    """ pretty print for gate sequence """
    return " ⊗ ".join([f"{gate.name}{_to_subscript(gate.args)}" for gate in gates])
