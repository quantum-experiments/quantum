from functools import reduce

import numpy as np

from quantum.grammar import parse, Qubits
from quantum.states import bit_states
from quantum.gates import name_gates, I
from quantum.formatter import pndarray

def bitstring_to_vector(qubits: str):
    """ Get kronecker product of basis vectors for given bitstring """
    qubits = [bit_states.get(bit) for bit in qubits]
    return reduce(np.kron, qubits)

def gate_by_name(name: str, args: tuple):
    """ get gate matrix representation by gate name and input arguments """
    if name == "CX":
        name = "CNOT"
    if name == "CNOT":
        control_target, = args
        return name_gates.get(name + control_target)
    return name_gates.get(name)

def _list_str(values):
    return ", ".join([str(val) for val in values])

def gates_to_unitary(gates, num_qubits):
    """ chain together single qubit gate ops into one unitary transformation """
    if all([len(gate.args)==1 and len(gate.args[0]) == 1 for gate in gates]):
        gate_seq = []
        gates_by_indices = {int(gate.args[0]): gate for gate in gates}
        assert all([ind < num_qubits for ind in gates_by_indices]), f"Got invalid index {_list_str(gates_by_indices.keys())}. For {num_qubits} qubits, valid indices are: {_list_str(range(num_qubits))}."
        for n in range(num_qubits):
            if n in gates_by_indices:
                gate = gates_by_indices.get(n)
                gate_seq.append(gate_by_name(gate.name, gate.args))
            else:
                gate_seq.append(I)
        return reduce(np.kron, gate_seq)
    gate, = gates
    return gate_by_name(gate.name, gate.args)

def evaluate_circuit(circuit):
    """ evaluate circuit and return qubit result """
    assert circuit.target.bitstring != "", "Cannot evaluate circuit: no qubits given"
    qubits = bitstring_to_vector(circuit.target.bitstring)
    if circuit.gates is None:
        return qubits
    num_qubits = len(circuit.target.bitstring)
    for gates in circuit.gates:
        qubits = np.dot(gates_to_unitary(gates, num_qubits), qubits)
    return qubits

def evaluate(line, pretty_print: bool = True):
    """
    evaluate line
    
    :pretty_print: flag to turn pretty printing off
    """
    circuit = parse(line)
    result = evaluate_circuit(circuit)
    if pretty_print:
        return result.view(pndarray)
    return result
