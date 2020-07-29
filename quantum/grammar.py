from collections import namedtuple

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(r"""
    circuit = circ* target
    circ = kronecker space
    target = kronecker / qubits / circuit
    kronecker = opkron* operation
    opkron = operation kron
    space = " "
    kron = "."
    operation = gate lbra args rbra
    qubits = qubits_open qubits_value qubits_close
    gate = ~"[A-Z]+"
    lbra = "["
    rbra = "]"
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
Circuit = namedtuple("Circuit", ["gates", "target"])
Gate = namedtuple("Gate", ["name", "args"])

class QuantumVisitor(NodeVisitor):
    """ Node visitor for Quantum grammar """
    def visit_circuit(self, node, visited_children):
        circs, (target,) = visited_children
        if len(circs) > 0:
            kronecker, _ = circs[-1]
            result = Circuit(
                gates=kronecker.gates,
                target=target.target)

            for circ in circs[::-1][1:]:
                kronecker, _ = circ
                result = Circuit(
                    gates=kronecker.gates, 
                    target=result)

            return result
        return target

    def visit_operation(self, node, visited_children):
        gate, _, args, _ = visited_children
        return Gate(name=gate, args=tuple(args))

    def visit_kronecker(self, node, visited_children):
        opkron, operation = visited_children
        if opkron:
            return Circuit(
                gates=tuple(opkron + [operation]), 
                target=None
            )
        return Circuit(gates=(operation, ), target=None)

    def visit_opkron(self, node, visited_children):
        operation, _ = visited_children
        return operation

    def visit_arg(self, node, visited_children):
        ind, _ = visited_children
        return ind

    def visit_qubits(self, node, visited_children):
        _, value, _ = node.children
        return Circuit(gates=None, target=Qubits(bitstring=value.text))
    
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node.text


def parse(command: str) -> Circuit:
    """ Parse given quantum command """
    return QuantumVisitor().visit(grammar.parse(command))
