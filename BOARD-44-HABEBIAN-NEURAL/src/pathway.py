"""
Habebian Pathway — the full neural pathway for MAT-225 Calc I
Modules 5→6→7→8 wired as a chain of neurons and synapses.

Like Physarum: signal reinforces the strongest path,
weak synapses get pruned (antibody triggered).
"""
from typing import List, Dict
from .neuron import Neuron
from .synapse import Synapse


class Pathway:
    def __init__(self, name: str):
        self.name = name
        self.neurons: Dict[str, Neuron] = {}
        self.synapses: List[Synapse] = []

    def add_neuron(self, neuron: Neuron) -> "Pathway":
        self.neurons[neuron.module_id] = neuron
        return self

    def connect(self, pre_id: str, post_id: str,
                supporting: int = 3, contradicting: int = 0) -> "Pathway":
        pre  = self.neurons[pre_id]
        post = self.neurons[post_id]
        syn  = Synapse(pre=pre, post=post,
                       label=f"{pre_id}→{post_id}",
                       supporting=supporting,
                       contradicting=contradicting)
        self.synapses.append(syn)
        return self

    def fire_all(self) -> List[dict]:
        results = []
        for neuron in self.neurons.values():
            results.append(neuron.fire())
        return results

    def transmit_all(self) -> List[dict]:
        return [s.transmit() for s in self.synapses]

    def status_report(self) -> dict:
        return {
            "pathway": self.name,
            "neurons": [n.status() for n in self.neurons.values()],
            "synapses": [
                {
                    "link": s.label,
                    "bond_order": s.bond_order,
                    "transmitted": s.pre.axon.fired,
                }
                for s in self.synapses
            ],
        }

    def sagco_command(self, cmd: str, *args) -> str:
        """
        Custom SAGCO commands:
          fire <module_id>           — fire a neuron
          receive <module_id> <label> — mark dendrite received
          status                     — print full pathway status
          synapse <pre> <post>       — show synapse bond order
          transmit                   — propagate all signals
          eru                        — run ERU across all neurons
        """
        if cmd == "fire":
            mid = args[0]
            result = self.neurons[mid].fire()
            return f"FIRE {mid}: strength={result['strength']} fired={result['fired']} eru={result['eru']}"

        elif cmd == "receive":
            mid, label = args[0], args[1]
            variance = float(args[2]) if len(args) > 2 else 0.0
            self.neurons[mid].receive(label, variance)
            return f"DENDRITE RECEIVED: {mid}/{label} variance={variance}"

        elif cmd == "status":
            report = self.status_report()
            lines = [f"PATHWAY: {report['pathway']}"]
            for n in report["neurons"]:
                lines.append(
                    f"  {n['module']} [{n['eru']}] "
                    f"strength={n['soma_strength']} "
                    f"due={n['due']} "
                    f"pending={n['pending']}"
                )
            for s in report["synapses"]:
                lines.append(
                    f"  SYNAPSE {s['link']} bond_order={s['bond_order']} "
                    f"{'LIVE' if s['transmitted'] else 'BLOCKED'}"
                )
            return "\n".join(lines)

        elif cmd == "synapse":
            pre_id, post_id = args[0], args[1]
            for s in self.synapses:
                if s.pre.module_id == pre_id and s.post.module_id == post_id:
                    r = s.transmit()
                    return f"SYNAPSE {r['synapse']}: transmitted={r['transmitted']} bond_order={r['bond_order']} eru={r['eru']}"
            return f"No synapse {pre_id}→{post_id}"

        elif cmd == "transmit":
            results = self.transmit_all()
            return "\n".join(
                f"SYNAPSE {r['synapse']}: {'LIVE signal_strength=' + str(r.get('signal_strength','')) if r['transmitted'] else 'BLOCKED — ' + r.get('reason','')}"
                for r in results
            )

        elif cmd == "eru":
            lines = []
            for n in self.neurons.values():
                n.fire()
                lines.append(f"  {n.module_id}: {n.soma.eru_label}")
            return "ERU PATHWAY AUDIT:\n" + "\n".join(lines)

        return f"Unknown command: {cmd}"
