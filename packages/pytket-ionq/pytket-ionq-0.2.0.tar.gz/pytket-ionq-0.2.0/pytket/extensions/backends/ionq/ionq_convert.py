# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

from pytket.passes import RebaseCustom  # type: ignore
from pytket.circuit import Circuit, OpType, Command  # type: ignore
from typing import Dict, Tuple, Any, List
from numpy import pi  # type: ignore


def _from_tk1(a: float, b: float, c: float) -> Circuit:
    circ = Circuit(1)
    circ.Rz(c, 0)
    circ.Rx(b, 0)
    circ.Rz(a, 0)
    return circ


ionq_multiqs = {
    OpType.SWAP,
    OpType.CX,
    OpType.ZZPhase,
    OpType.XXPhase,
    OpType.YYPhase,
    OpType.ZZMax,
    OpType.Barrier,
}
ionq_singleqs = {
    OpType.X,
    OpType.Y,
    OpType.Z,
    OpType.Rx,
    OpType.Ry,
    OpType.Rz,
    OpType.H,
    OpType.S,
    OpType.Sdg,
    OpType.T,
    OpType.Tdg,
    OpType.V,
    OpType.Vdg,
    OpType.Measure,
    OpType.noop,
}

ionq_gates = ionq_multiqs.union(ionq_singleqs)

ionq_pass = RebaseCustom(
    ionq_multiqs,
    Circuit(),  # cx_replacement (irrelevant)
    ionq_singleqs,  # singleqs
    _from_tk1,
)  # tk1_replacement

ionq_gate_dict = {
    OpType.X: "x",
    OpType.Y: "y",
    OpType.Z: "z",
    OpType.Rx: "rx",
    OpType.Ry: "ry",
    OpType.Rz: "rz",
    OpType.H: "h",
    OpType.CX: "cnot",
    OpType.S: "s",
    OpType.Sdg: "si",
    OpType.T: "t",
    OpType.Tdg: "ti",
    OpType.V: "v",
    OpType.Vdg: "vi",
    OpType.SWAP: "swap",
    OpType.ZZPhase: "zz",
    OpType.XXPhase: "xx",
    OpType.YYPhase: "yy",
    OpType.ZZMax: "zz",
}


# https://dewdrop.ionq.co/#quantum-programs
def command_to_ionq(com: Command) -> Dict:
    optype = com.op.type
    if optype not in ionq_gates:
        raise TypeError("Gate of type {} is not accepted by IonQ.".format(optype))
    gate_d: Dict[str, Any] = dict()
    gate_d["gate"] = ionq_gate_dict.get(optype)
    n_params = len(com.op.params)
    if n_params == 1:
        gate_d["rotation"] = pi * com.op.params[0]
    elif n_params > 1:
        raise TypeError(
            "Gate {} has {} parameters. Only 1 is allowed.".format(com.op, n_params)
        )
    if optype == OpType.ZZMax:
        gate_d["rotation"] = pi / 2
    qbs = com.qubits
    # CX is a special case in the IonQ json format
    if optype == OpType.CX:
        gate_d["control"] = qbs[0].index[0]
        gate_d["target"] = qbs[1].index[0]
    else:
        if len(qbs) == 1:
            gate_d["target"] = qbs[0].index[0]
        else:
            gate_d["targets"] = [q.index[0] for q in qbs]
    return gate_d


def tk_to_ionq(circ: Circuit) -> Tuple[Dict, List]:
    body = dict()
    body["qubits"] = circ.n_qubits
    circ_body: list = list()
    measures: list = list()
    for com in circ:
        # Measure gates are not valid input to the API
        # Circuits are assumed to all be measured at the end
        if com.op.type in (OpType.Barrier, OpType.noop):
            continue
        elif com.op.type == OpType.Measure:
            # predicate has already checked format is correct, so
            # errors are not handled here
            qb_id = com.qubits[0].index[0]
            bit_id = com.bits[0].index[0]
            while len(measures) <= bit_id:
                measures.append(None)
            measures[bit_id] = qb_id
        else:
            circ_body.append(command_to_ionq(com))
    body["circuit"] = circ_body
    if None in measures:
        raise IndexError("Bit index not written to by a measurement.")
    # if len(measures) != circ.n_qubits:
    # raise IndexError("Must measure all qubits.")
    return (body, measures)
