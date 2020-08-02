from functools import reduce

import logging
import numpy as np

from quantum.grammar import parse, Qubits
from quantum.states import bit_states
from quantum.gates import name_gates, I
from quantum.formatter import dirac, farray, pprint_kronecker_product

_log = logging.getLogger(__name__)

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
        gate_matrix = name_gates.get(name + control_target)
    else:
        gate_matrix = name_gates.get(name)

    if gate_matrix is not None:
        return gate_matrix

    raise ValueError(f"Gate {name} with args {args} not found.")

def _list_str(values):
    return ", ".join([str(val) for val in values])

def gates_to_unitary(gates, num_qubits):
    """ Get unitary transformation for one or more gates """
    # chain together single qubit gate ops into one unitary transformation
    if all([len(gate.args)==1 and len(gate.args[0]) == 1 for gate in gates]):
        if len(gates) != len(set(gates)):
            raise ValueError(f"Gate sequence contains duplicates: \
                {pprint_kronecker_product(gates)}")
        all_args = [arg for gate in gates for arg in gate.args]
        if len(all_args) != len(set(all_args)):
            raise ValueError(
                f"Cannot evaluate sequence that acts on the same qubit twice: \
                    {pprint_kronecker_product(gates)}")
        gate_seq = []
        gates_by_indices = {int(gate.args[0]): gate for gate in gates}
        assert all([ind < num_qubits for ind in gates_by_indices]), f"Got invalid index \
                {_list_str(gates_by_indices.keys())}. \
                For {num_qubits} qubits, valid indices are: \
                {_list_str(range(num_qubits))}."
        for n in range(num_qubits):
            if n in gates_by_indices:
                gate = gates_by_indices.get(n)
                gate_seq.append(gate_by_name(gate.name, gate.args))
            else:
                gate_seq.append(I)
        return reduce(np.kron, gate_seq)
    # single gate
    assert len(gates) == 1, f"Cannot get unitary transform for gates {gates} with \
        {num_qubits} qubits."
    gate, = gates
    return gate_by_name(gate.name, gate.args)

def all_args(circuit):
    """ get a flat list of all arguments passed to the circuit """
    return [arg for gates in circuit.gates for gate in gates for arg in gate.args]

def evaluate_circuit(circuit):
    """ evaluate circuit and return qubit result """
    if circuit.target is not None and circuit.target.bitstring != "":
        qubits = bitstring_to_vector(circuit.target.bitstring)
        if circuit.gates is None:
            return qubits
        num_qubits = len(circuit.target.bitstring)
        for gates in circuit.gates:
            qubits = np.dot(gates_to_unitary(gates, num_qubits), qubits)
        return qubits
    
    if circuit.gates is not None:
        args = [int(arg) for arg in all_args(circuit)]
        num_qubits = max(args) + 1
        return [gates_to_unitary(gates, num_qubits) for gates in circuit.gates]

def evaluate(line, pretty_print: bool = True):
    """
    evaluate line
    
    :pretty_print: flag to turn pretty printing off
    """
    circuit = parse(line)
    result = evaluate_circuit(circuit)
    if pretty_print:
        shape = np.shape(result)
        if len(shape) == 2:
            return result.view(dirac)
        elif isinstance(result, list):
            return [r.view(farray) for r in result]
        else:
            return result.view(farray)
    return result
