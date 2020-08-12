import numpy as np
import fractions

def _str_fraction_format_fn(value: float):
    return str(fractions.Fraction(value).limit_denominator())

def _latex_frac(numerator: str, denominator: str):
    return "\\frac{%s}{%s}" % (numerator, denominator)

def _latex_fraction_format_fn(value: float):
    frac = fractions.Fraction(value).limit_denominator()
    if frac.denominator != 1:
        return _latex_frac(frac.numerator, frac.denominator)
    return str(frac.numerator)

def _fraction_formatter(value: float, latex: bool = False):
    """ pretty print fraction value"""
    format_fn = _latex_fraction_format_fn if latex else _str_fraction_format_fn
    _im, _re = np.imag(value), np.real(value)
    if np.round(_im, 10) == 0:
        return format_fn(_re)
    elif np.round(_re, 10) == 0:
        return f"{format_fn(_im)}i"
    else:
        as_fraction_re = f"{format_fn(_re)}" if _re != 0 else ""
        as_fraction_im = f"{format_fn(np.abs(_im))}i"
        op = "+" if _im > 0 else "-"
        return f"({as_fraction_re}{op}{as_fraction_im})"

def _str_sqrt(nom):
    if nom != 1:
        return f"√{nom}"
    return str(nom)

def _latex_sqrt(nom, i: str = ""):
    return "\\sqrt{%s}{%s}" % nom, i

def _str_sqrt_format_fn(value: float, i: str):
    fraction = fractions.Fraction(value).limit_denominator()
    numerator = _str_sqrt(fraction.numerator) if fraction.numerator != 1 else (i or "1")
    denominator = _str_sqrt(fraction.denominator)
    return f"{numerator}/{denominator}"

def _latex_sqrt_format_fn(value: float, i: str):
    frac = fractions.Fraction(value).limit_denominator()
    if frac.denominator != 1:
        numerator = _latex_sqrt(frac.numerator) if frac.numerator != 1 else (i or "1")
        denominator = _latex_sqrt(frac.denominator)
        return _latex_frac(numerator, denominator)
    return _latex_sqrt(frac.numerator, i)

def _sqrt_formatter(value: float, latex: bool = False):
    """ pretty print fraction value with sqrt symbol """
    format_fn = _latex_sqrt_format_fn if latex else _str_sqrt_format_fn
    squared_value = value**2
    _im, _re = np.imag(value), np.real(value)
    sign = np.sign(value)

    if np.round(_im, 10) == 0:
        squared_value, i = _re**2, ""
    elif np.round(_re, 10) == 0:
        squared_value, i = _im**2, "i"
    else:
        # Skip formatting square root of imaginary value (e.g. √(1/2i))
        return _fraction_formatter(value, latex)

    sign = "-" if sign < 0 else ""
    return f"{sign}{format_fn(squared_value, i)}"

def pprint_fraction(value: float, no_sqrt: bool = False, width: int = None, latex: bool = False):
    """
    Pretty print for fractional and/or sqrt float values.
    Returns the shortest representation (e.g. "1/√2" or "4.1").

    :value: float value
    :no_sqrt: flag for not including sqrt terms
    :width: cell width
    :latex: flag to return value in latex format
    """
    formatters = [_fraction_formatter]
    if not no_sqrt:
        formatters.append(_sqrt_formatter)
    if not latex:
        formatters.append(lambda x, *args: str(x))

    formatted = [formatter(value, latex) for formatter in formatters]

    result = min(
        formatted, 
        key=lambda x: len(x)
    )

    if width:
        return result.rjust(width)
    return result

def pretty_farray(no_sqrt: bool = False):
    """
    context manager for pretty printing arrays with fractions and sqrt terms

    :no_sqrt: flag for not including sqrt terms
    """
    keys = ["float", "complex_kind"]
    kwargs = {"linewidth": 200}
    return np.printoptions(formatter={key: lambda x: pprint_fraction(x, no_sqrt, width=6) for key in keys}, **kwargs)

def array_to_latex(matrix, no_sqrt: bool = False):
    """ Convert array to Latex string """
    inner = " \\\\ ".join([" & ".join([pprint_fraction(col, latex=True) for col in row]) for row in matrix])
    return "$$\\begin{bmatrix} %s \\end{bmatrix}$$" % inner

class farray(np.ndarray):
    """ ndarray but with pretty printing of fractions and sqrt values """
    def __repr__(self):
        with pretty_farray():
            return super(farray, self).__repr__()

    def __str__(self):
        with pretty_farray():
            return super(farray, self).__str__()

    def _repr_latex_(self):
        return array_to_latex(self)
