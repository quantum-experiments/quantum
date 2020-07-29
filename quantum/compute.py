from functools import reduce

import numpy as np

from quantum.grammar import parse, Qubits
from quantum.states import bit_states
from quantum.gates import name_gates, I

def bitstring_to_vector(qubits: str):
    """ Get kronecker product of basis vectors for given bitstring """
    qubits = [bit_states.get(bit) for bit in qubits]
    return reduce(np.kron, qubits)

def gate_by_name(name: str, args: tuple):
    if name == "CX":
        name = "CNOT"
    if name == "CNOT":
        control_target, = args
        return name_gates.get(name + control_target)
    return name_gates.get(name)

def gates_to_unitary(gates, num_qubits):
    """ chain together single qubit gate ops into one unitary transformation """
    if all([len(gate.args)==1 and len(gate.args[0]) == 1 for gate in gates]):
        gate_seq = []
        gates_by_indices = {int(gate.args[0]): gate for gate in gates}
        assert all([ind < num_qubits for ind in gates_by_indices])
        for n in range(num_qubits):
            if n in gates_by_indices:
                gate = gates_by_indices.get(n)
                gate_seq.append(gate_by_name(gate.name, gate.args))
            else:
                gate_seq.append(I)
        return reduce(np.kron, gate_seq)
    gate, = gates
    return gate_by_name(gate.name, gate.args)

def transform(circuit):
    if isinstance(circuit.target, Qubits):
        return circuit.target
    return transform(circuit.target)

def evaluate_circuit(circuit):
    num_qubits = len(circuit.target.bitstring)
    qubits = bitstring_to_vector(circuit.target.bitstring)
    for gates in circuit.gates:
        qubits = np.dot(gates_to_unitary(gates, num_qubits), qubits)
    return qubits

def evaluate(text):
    circuit = parse(text)
    return evaluate_circuit(circuit)