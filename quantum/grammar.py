from collections import namedtuple
from functools import reduce

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(r"""
    circuit = circ* target
    circ = kronecker space
    target = kronecker / qubits / circuit
    kronecker = opkron* operation
    opkron = operation kron
    space = " "
    kron = "*"
    operation = gate args*
    qubits = qubits_open qubits_value qubits_close
    gate = ~"[A-Z]+"
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
            gates = reduce(lambda x, y: x+y, [c.gates for c, _ in circs[::-1]])

            if target.target is None:
                return Circuit(
                gates=target.gates + gates,
                target=target.target)

            return Circuit(
                gates=gates,
                target=target.target)

        return target

    def visit_operation(self, node, visited_children):
        gate, args = visited_children
        if args:
            args, = args
            return Gate(name=gate, args=tuple(args))
        return Gate(name=gate, args=())

    def visit_kronecker(self, node, visited_children):
        opkron, operation = visited_children
        if opkron:
            return Circuit(
                gates=[tuple(opkron + [operation])], 
                target=None
            )
        return Circuit(gates=[(operation, )], target=None)

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
