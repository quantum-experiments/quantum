
def _to_subscript(args: tuple):
    args_str = ",".join(args)
    return "_{%s}" %args_str

def pprint_gate_sequence(gates: tuple):
    """ pretty print for gate sequence """
    return " ⊗ ".join([f"{gate.name}{_to_subscript(gate.args)}" for gate in gates])
