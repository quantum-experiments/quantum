from collections import namedtuple

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(r"""
    quantum = circuit / kronecker / qubits
    circuit = kronecker space qubits
    kronecker = opkron* operation
    opkron = operation kron
    space = " "
    kron = "."
    operation = gate lpar args rpar
    qubits = qubits_open qubits_value qubits_close
    gate = ~"[A-Z]+"
    lpar = "("
    rpar = ")"
    args = arg+
    arg = ind sep*
    sep = ","
    ind = ~"[0-9]+"
    qubits_value = ~"[0-1]*"
    qubits_open = "|"
    qubits_close = ">"
    """
)

Circuit = namedtuple("Circuit", ["gates", "qubits"])
Gate = namedtuple("Gate", ["gate", "args"])

class QuantumVisitor(NodeVisitor):
    """ Node visitor for Quantum grammar """
    def visit_quantum(self, node, visited_children):
        result, = visited_children
        return Circuit(
            gates=result.gates,
            qubits=result.qubits
        )

    def visit_circuit(self, node, visited_children):
        kronecker, _, qubits = visited_children
        result = Circuit(
            gates=kronecker.gates, 
            qubits=qubits.qubits)
        return result

    def visit_operation(self, node, visited_children):
        gate, _, args, _ = visited_children
        return Gate(gate=gate, args=tuple(args))

    def visit_kronecker(self, node, visited_children):
        opkron, operation = visited_children
        if opkron:
            return Circuit(
                gates=tuple(opkron + [operation]), 
                qubits=None
            )
        return Circuit(gates=(operation, ), qubits=None)

    def visit_opkron(self, node, visited_children):
        operation, _ = visited_children
        return operation

    def visit_arg(self, node, visited_children):
        ind, _ = visited_children
        return ind

    def visit_qubits(self, node, visited_children):
        _, value, _ = node.children
        return Circuit(gates=None, qubits=value.text)
    
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node.text


def parse(command: str) -> Circuit:
    """ Parse given quantum command """
    return QuantumVisitor().visit(grammar.parse(command))
