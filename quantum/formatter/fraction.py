import numpy as np
import fractions

def _fraction_formatter(value: float):
    """ pretty print fraction value"""
    _im, _re = np.imag(value), np.real(value)
    if _im == 0:
        as_fraction = fractions.Fraction(_re).limit_denominator()
        return str(as_fraction)
    return str(np.round(value, 10))

def _sqrt_formatter(value: float):
    """ pretty print fraction value with sqrt symbol """
    squared_value = value**2
    _im, _re = np.imag(squared_value), np.real(squared_value)
    if _im == 0:
        fraction = fractions.Fraction(_re).limit_denominator()
        def _to_str(nom):
            if nom != 1:
                return f"√{nom}"
            return str(nom)
        
        sign = "-" if np.sign(value) == -1 else ""
        return f"{sign}{_to_str(fraction.numerator)}/{_to_str(fraction.denominator)}"
    return f"√{np.round(squared_value, 10)}"

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
