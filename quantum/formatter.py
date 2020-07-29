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
    
    return f"{_to_str(fraction.numerator)}/{_to_str(fraction.denominator)}"

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

def pretty_print(no_sqrt: bool = False):
    """
    context manager for pretty printing fractions

    :no_sqrt: flag for not including sqrt terms
    """
    if no_sqrt:
        return np.printoptions(formatter={'float': lambda x: pprint_fraction(x, no_sqrt)})
    return np.printoptions(formatter={'float': pprint_fraction})

class pndarray(np.ndarray):
    """ ndarray but with pretty printing of fractions and sqrt values """
    def __repr__(self):
        with pretty_print():
            return str(self)