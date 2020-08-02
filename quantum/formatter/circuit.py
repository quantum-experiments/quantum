import enum
from typing import TYPE_CHECKING, Tuple

from quantum.formatter.dirac import pprint_qubits

if TYPE_CHECKING:
    from quantum.grammar import Circuit, Matrix

class Symbols(enum.Enum):
    KRON = " ⨂ "
    DOT = " ∙ "
    SPACE = " "
    NONE = ""

_subscript = {
    "0": "₀",
    "1": "₁",
    "2": "₂",
    "3": "₃",
    "4": "₄",
    "5": "₅",
    "6": "₆",
    "7": "₇",
    "8": "₈",
    "9": "₉",
}

def _to_subscript(args: tuple, latex: bool = False) -> str:
    """ convert args to subscript """
    if latex:
        args_str = ",".join(args)
        return "_{%s}" %args_str
    return ",".join("".join([_subscript.get(_a) for _a in str(arg)]) for arg in args)

def pprint_matrix(matrix: 'Matrix'):
    return f"{matrix.label}{_to_subscript(matrix.args)}"

def pprint_kronecker_product(matrices: Tuple['Matrix']):
    """ pretty print for gate sequence """
    return Symbols.KRON.value.join([pprint_matrix(matrix) for matrix in matrices])

def pprint_circuit(circuit: 'Circuit'):
    """ pretty print circuit """
    result = ""
    for kron in circuit.kronecker_products:
        result += pprint_kronecker_product(kron.matrices)
        result += kron.operator.value
    
    if circuit.target:
        result += pprint_qubits(circuit.target.bitstring)

    return result
