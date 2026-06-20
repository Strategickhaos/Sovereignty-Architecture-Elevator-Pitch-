"""
Habebian Neuron — the core unit of the ecosystem
Each module in MAT-225 is a neuron.

Anatomy:
  dendrites  → receive incoming signals (assignments, readings, quizzes)
  soma       → integrate signals, run ERU, decide if threshold is met
  axon       → transmit result to next neuron (next module begins)
  synapse    → connection between axon of N and dendrite of N+1
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date


@dataclass
class Dendrite:
    """Receives a signal — one input per assignment/quiz/discussion"""
    signal_type: str          # "assignment" | "quiz" | "discussion" | "reading"
    label: str
    due_date: date
    weight: float = 1.0       # ERU weight (how much this fires the soma)
    received: bool = False    # has the signal arrived (submitted)?
    eru_variance: float = 0.0 # Expected-Reality variance on this signal


@dataclass
class Soma:
    """Integrates all dendrite signals, computes action potential"""
    threshold: float = 0.7    # fraction of weighted signals needed to fire
    eru_label: str = "PENDING"

    def integrate(self, dendrites: List[Dendrite]) -> float:
        if not dendrites:
            return 0.0
        total_weight = sum(d.weight for d in dendrites)
        received_weight = sum(d.weight for d in dendrites if d.received)
        return received_weight / total_weight if total_weight > 0 else 0.0

    def should_fire(self, dendrites: List[Dendrite]) -> bool:
        return self.integrate(dendrites) >= self.threshold


@dataclass
class Axon:
    """Transmits the firing signal to the next module's dendrites"""
    fires_on: date            # the date this axon transmits (module due date)
    fired: bool = False
    signal_strength: float = 0.0  # 0.0–1.0, set by soma integration
    output_label: str = ""        # what gets sent downstream


@dataclass
class Neuron:
    """One complete module-neuron in the Habebian ecosystem"""
    module_id: str            # "MODULE-5", "MODULE-6", etc.
    label: str                # human label
    begins: date              # when module opens
    due: date                 # assignment due date
    dendrites: List[Dendrite] = field(default_factory=list)
    soma: Soma = field(default_factory=Soma)
    axon: Optional[Axon] = None

    def __post_init__(self):
        if self.axon is None:
            self.axon = Axon(fires_on=self.due)

    def add_dendrite(self, signal_type: str, label: str, weight: float = 1.0) -> "Neuron":
        self.dendrites.append(Dendrite(
            signal_type=signal_type,
            label=label,
            due_date=self.due,
            weight=weight,
        ))
        return self

    def receive(self, label: str, variance: float = 0.0):
        """Mark a dendrite signal as received (assignment submitted)"""
        for d in self.dendrites:
            if d.label == label:
                d.received = True
                d.eru_variance = variance
                return
        raise KeyError(f"No dendrite named '{label}' in {self.module_id}")

    def fire(self) -> dict:
        """Integrate soma, fire axon if threshold met"""
        strength = self.soma.integrate(self.dendrites)
        self.axon.signal_strength = strength
        if self.soma.should_fire(self.dendrites):
            self.axon.fired = True
            self.axon.output_label = f"{self.module_id}_COMPLETE"
            self.soma.eru_label = "VARIANCE_0"
        else:
            self.soma.eru_label = "OPEN_VARIANCE"
        return {
            "module": self.module_id,
            "strength": round(strength, 3),
            "fired": self.axon.fired,
            "eru": self.soma.eru_label,
            "output": self.axon.output_label,
        }

    def status(self) -> dict:
        received = [d.label for d in self.dendrites if d.received]
        pending  = [d.label for d in self.dendrites if not d.received]
        return {
            "module": self.module_id,
            "label": self.label,
            "begins": str(self.begins),
            "due": str(self.due),
            "received": received,
            "pending": pending,
            "soma_strength": round(self.soma.integrate(self.dendrites), 3),
            "axon_fired": self.axon.fired,
            "eru": self.soma.eru_label,
        }
