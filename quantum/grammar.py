from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(r"""
    circuit = kronecker* space* qubits*
    kronecker = opkron+
    opkron = operation kron*
    space = " "
    kron = "."
    operation = gate lpar args rpar
    qubits = qubits_open qubits_value
    gate = ~"[A-Z]+"
    lpar = "("
    rpar = ")"
    args = arg+
    arg = ind sep*
    sep = ","
    ind = ~"[0-9]+"
    qubits_value = ~"[0-1]*"
    qubits_open = "0q"
    """
)

class QuantumVisitor(NodeVisitor):
    def visit_circuit(self, node, visited_children):
        kronecker, _, qubits = visited_children
        return { "gates": kronecker, "qubits": qubits }

    def visit_operation(self, node, visited_children):
        gate, _, args, _ = visited_children
        return {"gate": gate, "args": args}

    def visit_kronecker(self, node, visited_children):
        return visited_children

    def visit_opkron(self, node, visited_children):
        operation, _ = visited_children
        return operation

    def visit_arg(self, node, visited_children):
        ind, _ = visited_children
        return ind

    def visit_qubits(self, node, visited_children):
        _, value = node.children
        return value.text
    
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node.text
