from functools import reduce

import numpy as np

from quantum.grammar import parse
from quantum.states import bit_states
from quantum.gates import name_gates, I

def _get_qubits(qubits: str):
    """ Get kronecker product of basis vectors for given bitstring """
    qubits = [bit_states.get(bit) for bit in qubits]
    return reduce(np.kron, qubits)

def _get_gate(name: str, args: tuple):
    if name in ["CNOT", "CX"]:
        control_target, = args
        return name_gates.get(name + control_target)
    return name_gates.get(name)

def single_qubit_op(gate_operation: np.ndarray, qubit_num: int, num_qubits: int) -> np.ndarray:
    gate_seq = [I] * num_qubits
    gate_seq[qubit_num] = gate_operation
    op = reduce(np.kron, gate_seq)
    return op

def parse_unitary(circuit):
    # chain together single qubit gate ops into one transformation
    num_qubits = len(circuit.qubits)
    gate_seq = [I] * num_qubits
    transformations = []

    def _add_gate(gate_operation, args):
        for ind in args:
            gate_seq[int(ind)] = gate_operation

    for n, gate in enumerate(circuit.gates[::-1]):
        if np.all([len(arg) == 1 for arg in gate.args]):
            _add_gate(_get_gate(gate.name, gate.args), gate.args)
        else:
            transformations.append(_get_gate(gate.name, gate.args))
    
    transformations.append(reduce(np.kron, gate_seq))

    return transformations[::-1]

def evaluate_circuit(circuit):
    qubits = _get_qubits(circuit.qubits)
    transformations = parse_unitary(circuit)
    for transformation in transformations:
        qubits = np.dot(transformation, qubits)
    return qubits

def evaluate(text):
    circuit = parse(text)
    return evaluate_circuit(circuit)
