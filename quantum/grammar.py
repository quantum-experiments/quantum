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

class QuantumVisitor(NodeVisitor):
    def visit_quantum(self, node, visited_children):
        _result, = visited_children
        result = { "gates": None, "qubits": None }
        result.update(_result)
        return result

    def visit_circuit(self, node, visited_children):
        kronecker, _, qubits = visited_children
        result = {
            "gates": kronecker.get("gates"), 
            "qubits": qubits.get("qubits")
            }
        return result

    def visit_operation(self, node, visited_children):
        gate, _, args, _ = visited_children
        return {"gate": gate, "args": args}

    def visit_kronecker(self, node, visited_children):
        opkron, operation = visited_children
        if opkron:
            return {"gates": opkron + [operation]}
        return {"gates": [operation]}

    def visit_opkron(self, node, visited_children):
        operation, _ = visited_children
        return operation

    def visit_arg(self, node, visited_children):
        ind, _ = visited_children
        return ind

    def visit_qubits(self, node, visited_children):
        _, value, _ = node.children
        return {"qubits": value.text}
    
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node.text
