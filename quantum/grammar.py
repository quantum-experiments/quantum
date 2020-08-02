import enum
from collections import namedtuple
from functools import reduce
from typing import List

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from quantum.formatter.circuit import (Symbols, pprint_circuit,
                                       pprint_kronecker_product, pprint_matrix)
from quantum.formatter.dirac import pprint_qubits
from quantum.gates import num_qubits

_operators = {
    ".": Symbols.DOT,
    "∙": Symbols.DOT,
    " ": Symbols.SPACE,
    "": Symbols.NONE,
}

grammar = Grammar(r"""
    circuit = kronecker_product_op* (kronecker_product / qubits)
    kronecker_product_op = (kronecker_product dot) / (kronecker_product dot_math) / (kronecker_product space)
    kronecker_product = (matrix kronecker)* matrix
    space = " "
    dot = "."
    dot_math = "∙"
    kronecker = "*" / "⨂" / "⊗"
    matrix = label args*
    qubits = qubits_open qubits_value qubits_close
    label = ~"[A-Z]+"
    args = arg+
    arg = ind sep*
    sep = ","
    ind = ~"[0-9]+"
    qubits_value = ~"[-+0-1]*"
    qubits_open = "|"
    qubits_close = ">"
    """
)

Qubits = namedtuple("Qubits", ["bitstring"])
Qubits.__repr__ = lambda self: pprint_qubits(self.bitstring)
Circuit = namedtuple("Circuit", ["kronecker_products", "target"])
Circuit.__repr__ = lambda self: pprint_circuit(self)
KroneckerProductOp = namedtuple("KroneckerProductOp", ["matrices", "operator"])
KroneckerProductOp.__repr__ = lambda self: pprint_kronecker_product(self.matrices)
Matrix = namedtuple("Matrix", ["label", "args"])
Matrix.__repr__ = lambda self: pprint_matrix(self)

class QuantumVisitor(NodeVisitor):
    """ Node visitor for Quantum grammar """
    def visit_circuit_on_qubits(self, node, visited_children):
        """ circuit_on_qubits = circuit space qubits """
        circuit, _, qubits = visited_children
        return Circuit(kronecker_products=circuit.kronecker_products, target=qubits)
    
    def visit_circuit(self, node, visited_children):
        """ circuit = kronecker_product_op* (kronecker_product / qubits) """
        kronecker_product_ops, (target, ) = visited_children
        kronecker_product_ops = [KroneckerProductOp(
            matrices=kronecker_product,
            operator=_operators.get(operator)
        ) for ((kronecker_product, operator),) in kronecker_product_ops]

        if not isinstance(target, Qubits):
            kronecker_product_ops += [KroneckerProductOp(matrices=target, operator=Symbols.NONE)]
            target = None
 
        return Circuit(
            kronecker_products=tuple(kronecker_product_ops),
            target=target)

    def visit_kronecker_product(self, node, visited_children) -> tuple:
        """ kronecker_product = (matrix kronecker)* matrix """
        matrix_kronecker, matrix = visited_children
        if matrix_kronecker:
            return tuple(_m for _m, _ in matrix_kronecker) + (matrix, )
        return (matrix, )

    def visit_matrix(self, node, visited_children):
        """ matrix = label args* """
        label, args = visited_children
        if args:
            args, = args
            if num_qubits.get(label) > 1 and len(args) == 1:
                args = tuple(arg for arg in args[0])
                assert len(args) == 2, f"Cannot parse arguments '{visited_children[1][0][0]}' for matrix {label}, >2 arguments were found"
            return Matrix(label=label, args=tuple(int(arg) for arg in args))
        return Matrix(label=label, args=())

    def visit_arg(self, node, visited_children):
        ind, _ = visited_children
        return ind

    def visit_qubits(self, node, visited_children):
        _, value, _ = node.children
        return Qubits(bitstring=value.text)
    
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node.text


def parse(command: str) -> Circuit:
    """ Parse given quantum command """
    return QuantumVisitor().visit(grammar.parse(command))
