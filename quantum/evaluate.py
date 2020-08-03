import logging
from functools import reduce

import numpy as np

from quantum.formatter import dirac, farray, pprint_kronecker_product
from quantum.formatter.circuit import Symbols
from quantum.gates import I, name_gates
from quantum.grammar import Qubits, parse
from quantum.states import bit_states

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
        control, target = args
        control, target = control - min(args), target - min(args)
        gate_matrix = name_gates.get(f"{name}{control}{target}")
    else:
        gate_matrix = name_gates.get(name)

    if gate_matrix is not None:
        return gate_matrix

    raise ValueError(f"Gate {name} with args {args} not found.")

def _list_str(values):
    return ", ".join([str(val) for val in values])

def gates_to_unitary(gates, num_qubits):
    """ Get unitary transformation for one or more gates """
    # kronecker product of matrices into one unitary transformation
    if len(gates) != len(set(gates)):
        raise ValueError(f"Gate sequence contains duplicates: \
            {pprint_kronecker_product(gates)}")
    all_args = [arg for gate in gates for arg in gate.args]
    if len(all_args) != len(set(all_args)):
        raise ValueError(
            f"Cannot evaluate sequence that acts on the same qubit twice: \
                {pprint_kronecker_product(gates)}")
    gate_seq = [gate_by_name(gate.label, gate.args) for gate in gates]
    return reduce(np.kron, gate_seq)

def all_args(circuit):
    """ get a flat list of all arguments passed to the circuit """
    return [arg for kp in circuit.kronecker_products for gate in kp.matrices for arg in gate.args]

def evaluate_circuit(circuit):
    """ evaluate circuit and return qubit result """
    if circuit.target is not None and circuit.target.bitstring != "":
        qubits = bitstring_to_vector(circuit.target.bitstring)
        if circuit.kronecker_products is None:
            return qubits
        num_qubits = len(circuit.target.bitstring)
    else:
        args = [int(arg) for arg in all_args(circuit)]
        num_qubits = max(args) + 1

    if circuit.kronecker_products is not None:
        unitaries = [gates_to_unitary(kp.matrices, num_qubits) for kp in circuit.kronecker_products]

    if circuit.target is None:
        result, dot = [], False
        for kp, uni in zip(circuit.kronecker_products, unitaries):
            if dot:
                result.append(np.dot(result.pop(), uni))
            else:
                result.append(uni)
            dot = kp.operator == Symbols.DOT            
        return result
    return reduce(np.dot, unitaries + [qubits])

def evaluate(line, pretty_print: bool = True):
    """
    evaluate line
    
    :pretty_print: flag to turn pretty printing off
    """
    circuit = parse(line, expand=True)
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
