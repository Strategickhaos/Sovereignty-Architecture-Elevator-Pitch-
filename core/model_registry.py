"""
Model Registry for TRIG6
=========================
Provides documentation and metadata for computational models.
"""


class ModelRegistry:
    """Registry of computational models with documentation."""
    
    def __init__(self):
        self.models = {
            "trig6_vector": {
                "name": "Six Trigonometric Functions",
                "formula": "sin(θ), cos(θ), tan(θ), csc(θ), sec(θ), cot(θ)",
                "description": "Computes all six trigonometric functions for a given angle in degrees.",
                "inputs": ["theta_deg: angle in degrees"],
                "outputs": ["sin, cos, tan, csc, sec, cot"],
                "assumptions": ["theta measured in degrees"],
                "references": []
            },
            "bridle_two_leg_equal_angle": {
                "name": "Two-Leg Bridle Tension",
                "formula": "T = W / (2 * cos(θ/2))",
                "description": "Calculates leg tension in a symmetric two-leg bridle supporting a load. The included angle is the angle between the two legs.",
                "inputs": [
                    "load: vertical load in lbf",
                    "included_angle_deg: angle between legs in degrees"
                ],
                "outputs": ["leg_tension: tension in each leg (lbf)"],
                "assumptions": [
                    "two equal legs",
                    "symmetric configuration",
                    "no friction",
                    "static load"
                ],
                "safety_warnings": [
                    "Angles > 120° result in leg tension exceeding the load",
                    "Never exceed working load limits of equipment"
                ],
                "references": [
                    "NFPA 1983 - Standard on Life Safety Rope",
                    "Rigging for Rescue - Technical Rigging"
                ]
            },
            "highline_center_symmetric": {
                "name": "Symmetric Highline Tension",
                "formula": "T = W / (2 * sin(θ))",
                "description": "Calculates tension in each side of a symmetric highline with a center load. The sag angle is measured from horizontal.",
                "inputs": [
                    "load: vertical load in lbf",
                    "sag_angle_deg: angle from horizontal in degrees"
                ],
                "outputs": ["tension_each_side: tension in each side (lbf)"],
                "assumptions": [
                    "center load",
                    "symmetric legs",
                    "theta measured from horizontal"
                ],
                "safety_warnings": [
                    "Sag angles < 10° produce very high tensions",
                    "Small angle changes drastically affect tension"
                ],
                "references": [
                    "CMC Rope Rescue Manual",
                    "High Angle Rope Techniques"
                ]
            },
            "impact_field_estimate": {
                "name": "Impact Force Field Estimate",
                "formula": "F = W * (1 + sqrt(2 * FF))",
                "description": "Rough field estimate of impact force for falls on dynamic rope. Fall factor is the ratio of fall distance to rope length.",
                "inputs": [
                    "weight: climber weight in lbf",
                    "fall_factor: dimensionless ratio (0-2)"
                ],
                "outputs": ["impact_force: estimated peak force (lbf)"],
                "assumptions": [
                    "dynamic rope behavior",
                    "low-stretch systems produce higher peaks"
                ],
                "safety_warnings": [
                    "This is a field estimate only",
                    "Use manufacturer data for critical applications",
                    "Static rope can produce 10-15× higher forces"
                ],
                "references": [
                    "UIAA standards",
                    "Freedom of the Hills"
                ]
            },
            "angle_amplification_sec": {
                "name": "Angle Amplification (Secant)",
                "formula": "F_amplified = F / cos(θ)",
                "description": "Force amplification when pulling at an angle from vertical. The amplified force is the force on the anchor.",
                "inputs": [
                    "force: applied force in lbf",
                    "theta_from_vertical_deg: angle from vertical in degrees"
                ],
                "outputs": ["amplified_force: force on anchor (lbf)"],
                "assumptions": [
                    "theta measured from vertical",
                    "component resolution"
                ],
                "safety_warnings": [
                    "Large angles significantly amplify forces on anchors"
                ],
                "references": []
            },
            "mechanical_advantage_ideal": {
                "name": "Mechanical Advantage (Ideal)",
                "formula": "Pull = Load / MA",
                "description": "Calculates required pull force for a given mechanical advantage system. MA is determined by counting rope strands supporting the load.",
                "inputs": [
                    "load: load to lift in lbf",
                    "ma: mechanical advantage ratio"
                ],
                "outputs": ["pull: required pull force (lbf)"],
                "assumptions": [
                    "ideal system (no friction)",
                    "count strands supporting moving load"
                ],
                "safety_warnings": [
                    "Real pulleys have friction losses (5-50% per pulley)",
                    "Efficiency degrades with complexity"
                ],
                "references": [
                    "CMC Rope Rescue Manual",
                    "Technical Rescue Riggers Guide"
                ]
            },
            "multi_leg_equal_share_equal_angle": {
                "name": "Multi-Leg Equal Share",
                "formula": "T_per_leg = (Load / n) / cos(θ)",
                "description": "Tension per leg in a multi-leg anchor where load is equally shared and all legs have the same angle from vertical.",
                "inputs": [
                    "load: total load in lbf",
                    "n: number of legs",
                    "theta_from_vertical_deg: leg angle from vertical"
                ],
                "outputs": ["tension_per_leg: tension in each leg (lbf)"],
                "assumptions": [
                    "equal load sharing",
                    "identical leg angles",
                    "not for unequal geometry"
                ],
                "safety_warnings": [
                    "Perfect equal sharing rarely occurs in practice",
                    "Assume worst-case single-point loading for safety"
                ],
                "references": [
                    "NFPA 1983",
                    "SPRAT Safe Practices"
                ]
            }
        }
    
    def list_models(self) -> list:
        """List all registered model IDs."""
        return list(self.models.keys())
    
    def explain(self, model_id: str) -> str:
        """Get detailed explanation of a model."""
        model = self.models.get(model_id)
        if not model:
            return f"Unknown model: {model_id}\n\nAvailable models:\n" + "\n".join(f"  - {m}" for m in self.list_models())
        
        lines = [
            f"MODEL: {model['name']}",
            f"ID: {model_id}",
            "",
            f"FORMULA: {model['formula']}",
            "",
            f"DESCRIPTION:",
            f"  {model['description']}",
            "",
            "INPUTS:"
        ]
        
        for inp in model['inputs']:
            lines.append(f"  - {inp}")
        
        lines.append("")
        lines.append("OUTPUTS:")
        for out in model['outputs']:
            lines.append(f"  - {out}")
        
        lines.append("")
        lines.append("ASSUMPTIONS:")
        for assum in model['assumptions']:
            lines.append(f"  - {assum}")
        
        if model.get('safety_warnings'):
            lines.append("")
            lines.append("⚠️  SAFETY WARNINGS:")
            for warn in model['safety_warnings']:
                lines.append(f"  - {warn}")
        
        if model.get('references'):
            lines.append("")
            lines.append("REFERENCES:")
            for ref in model['references']:
                lines.append(f"  - {ref}")
        
        return "\n".join(lines)
