# Copyright 2020-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html

from qiskit.assembler import disassemble  # type: ignore
from qiskit.providers import BaseBackend  # type: ignore
from qiskit.providers.models import QasmBackendConfiguration  # type: ignore
from qiskit.qobj import QasmQobj  # type: ignore

from pytket.extensions.qiskit.qiskit_convert import qiskit_to_tk, _gate_str_2_optype_rev
from pytket.extensions.qiskit.tket_job import TketJob

from pytket.circuit import OpType  # type: ignore
from pytket.backends import Backend
from pytket.passes import BasePass  # type: ignore
from pytket.predicates import (  # type: ignore
    NoClassicalControlPredicate,
    GateSetPredicate,
    CompilationUnit,
)

from typing import Optional, List


def _extract_basis_gates(backend: Backend) -> List[str]:
    for pred in backend.required_predicates:
        if type(pred) == GateSetPredicate:
            return [
                _gate_str_2_optype_rev[optype]
                for optype in pred.gate_set
                if optype in _gate_str_2_optype_rev.keys()
            ]
    return []


class TketBackend(BaseBackend):
    """TketBackend wraps a :py:class:`Backend` as a :py:class:`qiskit.providers.BaseBackend`"""

    def __init__(self, backend: Backend, comp_pass: Optional[BasePass] = None):
        config = QasmBackendConfiguration(
            backend_name=("statevector_" if backend.supports_state else "")
            + "pytket/"
            + str(type(backend)),
            backend_version="0.0.1",
            n_qubits=len(backend.device.nodes) if backend.device else 40,
            basis_gates=_extract_basis_gates(backend),
            gates=[],
            local=False,
            simulator=False,
            conditional=not any(
                (
                    type(pred) == NoClassicalControlPredicate
                    for pred in backend.required_predicates
                )
            ),
            open_pulse=False,
            memory=backend.supports_shots,
            max_shots=10000,
            coupling_map=[[n.index[0], m.index[0]] for n, m in backend.device.coupling]
            if backend.device
            else None,
            max_experiments=10000,
        )
        super().__init__(configuration=config, provider=None)
        self._backend = backend
        self._comp_pass = comp_pass

    def run(self, qobj: QasmQobj) -> TketJob:
        module = disassemble(qobj)
        circ_list = [qiskit_to_tk(qc) for qc in module[0]]
        if self._comp_pass:
            final_maps = []
            compiled_list = []
            for c in circ_list:
                cu = CompilationUnit(c)
                self._comp_pass.apply(cu)
                compiled_list.append(cu.circuit)
                final_maps.append(cu.final_map)
            circ_list = compiled_list
        else:
            final_maps = [None for c in circ_list]
        handles = self._backend.process_circuits(circ_list, n_shots=qobj.config.shots)
        return TketJob(self, handles, qobj, final_maps)
