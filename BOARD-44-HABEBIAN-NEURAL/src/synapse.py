"""
Synapse — the connection between two neurons (modules)
Signal from axon of N travels through synapse to dendrites of N+1.

Bond Order (from SAGCO-UNIVERSITY):
  bond_order = (supporting_signals - contradicting_signals) / 2

A strong synapse = high bond order = clean transition between modules.
A weak synapse = low bond order = gap in understanding (needs antibody).
"""
from dataclasses import dataclass
from .neuron import Neuron


@dataclass
class Synapse:
    pre:  Neuron    # upstream neuron (source axon)
    post: Neuron    # downstream neuron (target dendrites)
    label: str = ""
    supporting: int = 0    # concepts that carry forward cleanly
    contradicting: int = 0 # gaps or unresolved variance

    @property
    def bond_order(self) -> float:
        return (self.supporting - self.contradicting) / 2

    def transmit(self) -> dict:
        """Fire signal from pre-axon into post-dendrites if pre fired"""
        if not self.pre.axon.fired:
            return {
                "synapse": f"{self.pre.module_id}→{self.post.module_id}",
                "transmitted": False,
                "reason": f"{self.pre.module_id} axon has not fired",
                "bond_order": self.bond_order,
            }
        signal = self.pre.axon.signal_strength
        return {
            "synapse": f"{self.pre.module_id}→{self.post.module_id}",
            "transmitted": True,
            "signal_strength": round(signal, 3),
            "bond_order": self.bond_order,
            "eru": "VARIANCE_0" if self.bond_order >= 0 else "OPEN_VARIANCE",
        }
