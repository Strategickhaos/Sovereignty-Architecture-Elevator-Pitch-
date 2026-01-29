#!/usr/bin/env python3
"""
TRIG6 Model Registry
====================
Every computational model must declare:
- Its name (unique identifier)
- Its assumptions (what must be true for the model to be valid)
- Its required inputs (with units)
- Its outputs (with units)
- Its limitations (when NOT to use it)

This separation keeps "math" clean and "provenance" auditable.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
"""

from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional, Any
from enum import Enum


class ModelCategory(Enum):
    """Categories of computational models."""
    TRIG = "trigonometry"
    ROPE = "rope_mechanics"
    RIGGING = "rigging"
    PIPE = "pipefitting"
    NDT = "ndt"
    KHAOS = "khaos_symbolic"


@dataclass
class ModelInput:
    """Definition of a model input parameter."""
    name: str
    description: str
    units: str                    # e.g., "lbf", "degrees", "ratio"
    required: bool = True
    default: Optional[Any] = None
    valid_range: Optional[tuple] = None  # (min, max) or None


@dataclass
class ModelOutput:
    """Definition of a model output field."""
    name: str
    description: str
    units: str


@dataclass
class ModelDefinition:
    """
    Complete definition of a computational model.
    
    This is the "contract" that every model must fulfill.
    Auditors can inspect this without running the code.
    """
    id: str                       # Unique identifier (e.g., "bridle_two_leg_equal_angle")
    name: str                     # Human-readable name
    category: ModelCategory
    description: str              # What it computes
    formula: str                  # Mathematical formula (LaTeX or plain)
    assumptions: List[str]        # What must be true for this to be valid
    limitations: List[str]        # When NOT to use this model
    inputs: List[ModelInput]
    outputs: List[ModelOutput]
    citations: List[str] = field(default_factory=list)  # Keys into constants registry
    version: str = "1.0.0"
    
    def validate_inputs(self, **kwargs) -> List[str]:
        """Check that inputs are valid. Returns list of errors."""
        errors = []
        
        for inp in self.inputs:
            if inp.required and inp.name not in kwargs:
                errors.append(f"Missing required input: {inp.name}")
            
            if inp.name in kwargs and inp.valid_range:
                val = kwargs[inp.name]
                min_v, max_v = inp.valid_range
                if not (min_v <= val <= max_v):
                    errors.append(
                        f"{inp.name}={val} outside valid range [{min_v}, {max_v}]"
                    )
        
        return errors
    
    def to_dict(self) -> dict:
        """Serialize for JSON output."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "formula": self.formula,
            "assumptions": self.assumptions,
            "limitations": self.limitations,
            "inputs": [
                {
                    "name": i.name,
                    "description": i.description,
                    "units": i.units,
                    "required": i.required,
                    "valid_range": list(i.valid_range) if i.valid_range else None,
                }
                for i in self.inputs
            ],
            "outputs": [
                {"name": o.name, "description": o.description, "units": o.units}
                for o in self.outputs
            ],
            "citations": self.citations,
            "version": self.version,
        }


# ============================================================
# MODEL REGISTRY (singleton)
# ============================================================

class ModelRegistry:
    """
    Central registry of all computational models.
    
    Models must be registered before they can be used.
    This ensures every computation is documented.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._models = {}
            cls._instance._register_builtin_models()
        return cls._instance
    
    def _register_builtin_models(self):
        """Register all built-in TRIG6 models."""
        
        # TRIG6 Vector
        self.register(ModelDefinition(
            id="trig6_vector",
            name="TRIG6 Vector",
            category=ModelCategory.TRIG,
            description="Compute all six trigonometric functions for an angle",
            formula="[sin(θ), cos(θ), tan(θ), csc(θ), sec(θ), cot(θ)]",
            assumptions=[
                "θ is measured in degrees",
                "Standard mathematical conventions apply",
            ],
            limitations=[
                "tan(θ) undefined at θ = 90°, 270° (returns inf)",
                "cot(θ) undefined at θ = 0°, 180° (returns inf)",
            ],
            inputs=[
                ModelInput("theta_deg", "Angle in degrees", "degrees", 
                          valid_range=(-360, 360)),
            ],
            outputs=[
                ModelOutput("sin", "Sine of θ", "ratio"),
                ModelOutput("cos", "Cosine of θ", "ratio"),
                ModelOutput("tan", "Tangent of θ", "ratio"),
                ModelOutput("csc", "Cosecant of θ", "ratio"),
                ModelOutput("sec", "Secant of θ", "ratio"),
                ModelOutput("cot", "Cotangent of θ", "ratio"),
            ],
        ))
        
        # Bridle Two-Leg Equal Angle
        self.register(ModelDefinition(
            id="bridle_two_leg_equal_angle",
            name="Two-Leg Bridle Tension",
            category=ModelCategory.ROPE,
            description="Calculate leg tension in a symmetric two-leg bridle",
            formula="T = W / (2 × cos(θ/2))",
            assumptions=[
                "Two legs of equal length",
                "Symmetric loading (load at center)",
                "θ is the included angle between legs",
                "Static load (no dynamic/shock)",
                "No friction at attachment points",
                "Rigid attachment points",
            ],
            limitations=[
                "NOT valid for unequal leg lengths",
                "NOT valid for off-center loads",
                "NOT valid for dynamic loading without additional factors",
                "θ > 120° is dangerous (leg tension exceeds load)",
            ],
            inputs=[
                ModelInput("load", "Total load supported by bridle", "lbf"),
                ModelInput("included_angle_deg", "Included angle between legs", "degrees",
                          valid_range=(0, 175)),
            ],
            outputs=[
                ModelOutput("leg_tension", "Tension in each leg", "lbf"),
            ],
            citations=["rope.angle.max_bridle_included"],
        ))
        
        # Highline Center Symmetric
        self.register(ModelDefinition(
            id="highline_center_symmetric",
            name="Highline Tension (Symmetric)",
            category=ModelCategory.ROPE,
            description="Calculate tension in a symmetric highline with center load",
            formula="T = W / (2 × sin(θ))",
            assumptions=[
                "Load at center of span",
                "Symmetric sag on both sides",
                "θ is sag angle from horizontal",
                "Static load",
                "Anchors at same elevation",
            ],
            limitations=[
                "NOT valid for off-center loads",
                "NOT valid for anchors at different elevations",
                "Small sag angles produce very high tensions (θ < 10° is dangerous)",
                "Does not account for rope weight",
            ],
            inputs=[
                ModelInput("load", "Load at center of highline", "lbf"),
                ModelInput("sag_angle_deg", "Sag angle from horizontal", "degrees",
                          valid_range=(1, 89)),
            ],
            outputs=[
                ModelOutput("tension_each_side", "Tension on each side of load", "lbf"),
            ],
        ))
        
        # Impact Force Estimate
        self.register(ModelDefinition(
            id="impact_field_estimate",
            name="Impact Force (Field Estimate)",
            category=ModelCategory.ROPE,
            description="Estimate peak impact force from a fall",
            formula="F = W × (1 + √(2 × FF))",
            assumptions=[
                "Dynamic rope system (absorbs energy)",
                "Fall Factor (FF) = fall distance / rope in system",
                "Simplified field model",
            ],
            limitations=[
                "Underestimates forces in static/low-stretch rope systems",
                "Does not account for edge loads, friction, or redirection",
                "Actual forces depend on rope modulus, which varies",
                "Use manufacturer data for precise calculations",
            ],
            inputs=[
                ModelInput("weight", "Falling mass weight", "lbf"),
                ModelInput("fall_factor", "Fall factor (fall dist / rope length)", "ratio",
                          valid_range=(0, 2)),
            ],
            outputs=[
                ModelOutput("impact_force", "Estimated peak impact force", "lbf"),
            ],
        ))
        
        # Angle Amplification
        self.register(ModelDefinition(
            id="angle_amplification_sec",
            name="Angle Amplification (Secant)",
            category=ModelCategory.ROPE,
            description="Calculate force amplification when load is angled from vertical",
            formula="F_amp = F / cos(θ) = F × sec(θ)",
            assumptions=[
                "θ is angle from vertical",
                "Force must resolve along angled line",
                "Static equilibrium",
            ],
            limitations=[
                "Amplification grows rapidly as θ approaches 90°",
                "At θ = 90°, amplification is infinite (horizontal line cannot support vertical load)",
            ],
            inputs=[
                ModelInput("force", "Applied force", "lbf"),
                ModelInput("theta_from_vertical_deg", "Angle from vertical", "degrees",
                          valid_range=(0, 89)),
            ],
            outputs=[
                ModelOutput("amplified_force", "Force in angled member", "lbf"),
            ],
        ))
        
        # Mechanical Advantage
        self.register(ModelDefinition(
            id="mechanical_advantage_ideal",
            name="Mechanical Advantage (Ideal)",
            category=ModelCategory.ROPE,
            description="Calculate pull force required for given MA",
            formula="Pull = Load / MA",
            assumptions=[
                "Ideal system (no friction)",
                "MA = number of strands supporting the moving load",
                "Pulleys are 100% efficient",
            ],
            limitations=[
                "Real pulleys have friction (typically 90-95% efficient)",
                "Carabiners as pulleys are ~50% efficient",
                "Compound systems require separate efficiency calculation",
            ],
            inputs=[
                ModelInput("load", "Load to be moved", "lbf"),
                ModelInput("ma", "Mechanical advantage ratio", "ratio",
                          valid_range=(1, 20)),
            ],
            outputs=[
                ModelOutput("pull", "Required pull force", "lbf"),
            ],
            citations=["rope.pulley.efficiency.standard"],
        ))
        
        # Multi-Leg Equal Share
        self.register(ModelDefinition(
            id="multi_leg_equal_share_equal_angle",
            name="Multi-Leg Equal Share Tension",
            category=ModelCategory.RIGGING,
            description="Calculate leg tension for multi-point lift with equal angles",
            formula="T = (W/n) / cos(θ)",
            assumptions=[
                "All legs share load equally (symmetric geometry)",
                "All legs at same angle from vertical",
                "θ is angle from vertical (not between legs)",
                "Static load",
            ],
            limitations=[
                "NOT valid for unequal leg lengths",
                "NOT valid for unequal angles",
                "Real loads rarely share perfectly equally",
                "Use rigorous analysis for critical lifts",
            ],
            inputs=[
                ModelInput("load", "Total load", "lbf"),
                ModelInput("n", "Number of legs", "count", valid_range=(2, 8)),
                ModelInput("theta_from_vertical_deg", "Leg angle from vertical", "degrees",
                          valid_range=(0, 60)),
            ],
            outputs=[
                ModelOutput("tension_per_leg", "Tension in each leg", "lbf"),
            ],
            citations=["rigging.sling_angle.multiplier.60deg"],
        ))
    
    def register(self, model: ModelDefinition):
        """Register a model definition."""
        self._models[model.id] = model
    
    def get(self, model_id: str) -> Optional[ModelDefinition]:
        """Get a model definition by ID."""
        return self._models.get(model_id)
    
    def list_models(self, category: Optional[ModelCategory] = None) -> List[str]:
        """List all registered model IDs, optionally filtered by category."""
        if category:
            return [m.id for m in self._models.values() if m.category == category]
        return list(self._models.keys())
    
    def explain(self, model_id: str) -> str:
        """Get human-readable explanation of a model."""
        model = self.get(model_id)
        if not model:
            return f"Unknown model: {model_id}"
        
        lines = [
            f"MODEL: {model.name}",
            f"ID: {model.id}",
            f"CATEGORY: {model.category.value}",
            "",
            f"DESCRIPTION: {model.description}",
            f"FORMULA: {model.formula}",
            "",
            "ASSUMPTIONS:",
        ]
        for a in model.assumptions:
            lines.append(f"  • {a}")
        
        lines.append("")
        lines.append("LIMITATIONS:")
        for l in model.limitations:
            lines.append(f"  ⚠ {l}")
        
        lines.append("")
        lines.append("INPUTS:")
        for i in model.inputs:
            req = "(required)" if i.required else "(optional)"
            rng = f" [{i.valid_range[0]}-{i.valid_range[1]}]" if i.valid_range else ""
            lines.append(f"  • {i.name} [{i.units}]{rng} {req}")
            lines.append(f"    {i.description}")
        
        lines.append("")
        lines.append("OUTPUTS:")
        for o in model.outputs:
            lines.append(f"  • {o.name} [{o.units}]: {o.description}")
        
        if model.citations:
            lines.append("")
            lines.append("RELATED CONSTANTS:")
            for c in model.citations:
                lines.append(f"  → {c}")
        
        return "\n".join(lines)


# ============================================================
# SELF-TEST
# ============================================================

if __name__ == "__main__":
    print("=== TRIG6 Model Registry Self-Test ===\n")
    
    registry = ModelRegistry()
    
    print("Registered models:")
    for mid in registry.list_models():
        model = registry.get(mid)
        print(f"  • {mid} ({model.category.value})")
    
    print("\n" + "="*50)
    print(registry.explain("bridle_two_leg_equal_angle"))
    
    print("\n" + "="*50)
    print("\nInput validation test:")
    model = registry.get("bridle_two_leg_equal_angle")
    
    # Valid inputs
    errors = model.validate_inputs(load=300, included_angle_deg=120)
    print(f"  Valid inputs: {len(errors)} errors")
    
    # Missing input
    errors = model.validate_inputs(load=300)
    print(f"  Missing angle: {errors}")
    
    # Out of range
    errors = model.validate_inputs(load=300, included_angle_deg=180)
    print(f"  Angle=180: {errors}")
    
    print("\n✓ Model registry tests passed")
