"""
TRIG6 Model Registry
7 deterministic physics models with assumptions and limitations
"""

import math
from .units import Force, Angle, Length, validate_positive, validate_range


class PhysicsModel:
    """Base class for physics models"""
    
    def __init__(self, name, description, assumptions, limitations):
        self.name = name
        self.description = description
        self.assumptions = assumptions
        self.limitations = limitations
    
    def compute(self, **kwargs):
        """Compute the model - must be implemented by subclasses"""
        raise NotImplementedError
    
    def explain(self):
        """Explain the model with assumptions and limitations"""
        lines = []
        lines.append(f"\nMODEL: {self.name}")
        lines.append(f"DESCRIPTION: {self.description}")
        lines.append("\nASSUMPTIONS:")
        for assumption in self.assumptions:
            lines.append(f"  - {assumption}")
        lines.append("\nLIMITATIONS:")
        for limitation in self.limitations:
            lines.append(f"  - {limitation}")
        return '\n'.join(lines)


class VectorModel(PhysicsModel):
    """Model 1: All 6 trigonometric functions for a vector"""
    
    def __init__(self):
        super().__init__(
            name="vector",
            description="Calculate all 6 trig functions (sin, cos, tan, csc, sec, cot) for an angle",
            assumptions=[
                "Angle is measured in degrees from horizontal",
                "Right triangle trigonometry applies",
                "Unit circle conventions"
            ],
            limitations=[
                "Angles at 0°, 90°, 180°, 270° may have undefined values for some functions",
                "Results subject to floating point precision"
            ]
        )
    
    def compute(self, theta):
        """Compute all 6 trig functions"""
        angle = Angle(theta, 'degrees')
        rad = angle.to_radians()
        
        sin_val = math.sin(rad)
        cos_val = math.cos(rad)
        
        result = {
            'sin': sin_val,
            'cos': cos_val,
            'tan': math.tan(rad) if abs(cos_val) > 1e-10 else float('inf'),
            'csc': 1/sin_val if abs(sin_val) > 1e-10 else float('inf'),
            'sec': 1/cos_val if abs(cos_val) > 1e-10 else float('inf'),
            'cot': 1/math.tan(rad) if abs(math.tan(rad)) > 1e-10 else float('inf')
        }
        return result


class BridleTwoLegModel(PhysicsModel):
    """Model 2: Two-leg bridle with equal angles"""
    
    def __init__(self):
        super().__init__(
            name="bridle_two_leg_equal_angle",
            description="Calculate tension in two-leg bridle with equal leg angles",
            assumptions=[
                "Both legs have equal angle from vertical",
                "Load is centered",
                "Legs have equal length",
                "Static equilibrium"
            ],
            limitations=[
                "Does not account for dynamic loads",
                "Assumes massless rigging",
                "Angles > 60° from vertical require extreme caution",
                "Valid for angles 0° to 90° from vertical"
            ]
        )
    
    def compute(self, load, theta):
        """
        Compute tension in each leg
        load: total load in lbf
        theta: angle from vertical in degrees
        Returns: tension in each leg (lbf)
        """
        validate_positive(load, "load")
        validate_range(theta, 0, 90, "theta")
        
        angle = Angle(theta, 'degrees')
        rad = angle.to_radians()
        
        # T = W / (2 * cos(θ))
        tension = load / (2 * math.cos(rad))
        
        return {
            'tension_per_leg': tension,
            'total_tension': tension * 2,
            'angle_from_vertical': theta,
            'load': load,
            'warning': "CAUTION: High angle!" if theta > 60 else None
        }


class HighlineModel(PhysicsModel):
    """Model 3: Highline tension based on sag"""
    
    def __init__(self):
        super().__init__(
            name="highline_tension",
            description="Calculate tension in a highline based on load and sag",
            assumptions=[
                "Load is centered on span",
                "Catenary effect is minimal (small sag)",
                "Static load only",
                "Anchors are at same height"
            ],
            limitations=[
                "Simplified model - actual catenary calculations are more complex",
                "Does not account for rope stretch",
                "Valid for sag < 10% of span length",
                "Does not include safety factors"
            ]
        )
    
    def compute(self, load, sag, span=100):
        """
        Compute highline tension
        load: load in lbf
        sag: vertical sag in feet
        span: horizontal span in feet (default 100)
        Returns: tension in lbf
        """
        validate_positive(load, "load")
        validate_positive(sag, "sag")
        validate_positive(span, "span")
        
        # T = W * (L / (8 * sag)) for small angles
        # More accurate: T = W * sqrt(1 + (L/(2*sag))^2) / 2
        
        # Using the geometric formula
        half_span = span / 2
        tension = load * math.sqrt(1 + (half_span / sag) ** 2) / 2
        
        sag_ratio = sag / span
        
        return {
            'tension': tension,
            'load': load,
            'sag': sag,
            'span': span,
            'sag_ratio': sag_ratio,
            'warning': "Sag ratio too high!" if sag_ratio > 0.1 else None
        }


class ImpactForceModel(PhysicsModel):
    """Model 4: Fall impact force calculation"""
    
    def __init__(self):
        super().__init__(
            name="fall_impact_force",
            description="Calculate impact force for fall arrest systems",
            assumptions=[
                "Fall factor is defined as fall distance / rope length",
                "Rope has linear elasticity (simplified)",
                "No slack in system",
                "Instant deceleration at max extension"
            ],
            limitations=[
                "Actual fall arrest is complex with dynamic rope behavior",
                "Does not account for knot efficiency",
                "Ignores friction and air resistance",
                "Use certified fall protection equipment per ANSI Z359"
            ]
        )
    
    def compute(self, weight, fall_factor, rope_length=10):
        """
        Compute impact force
        weight: climber weight in lbf
        fall_factor: fall distance / rope length (0 to 2)
        rope_length: available rope in feet
        """
        validate_positive(weight, "weight")
        validate_range(fall_factor, 0, 2, "fall_factor")
        validate_positive(rope_length, "rope_length")
        
        # Simplified: F = W * (1 + sqrt(1 + 2h/d))
        # where h = fall distance, d = rope elongation
        # For dynamic rope, assume 30% elongation
        elongation_ratio = 0.30
        fall_distance = fall_factor * rope_length
        elongation = rope_length * elongation_ratio
        
        if elongation > 0:
            impact_force = weight * (1 + math.sqrt(1 + 2 * fall_distance / elongation))
        else:
            impact_force = weight * 10  # Extremely high if no elongation
        
        return {
            'impact_force': impact_force,
            'weight': weight,
            'fall_factor': fall_factor,
            'fall_distance': fall_distance,
            'estimated_elongation': elongation,
            'warning': "CRITICAL FALL FACTOR!" if fall_factor > 1 else None
        }


class MechanicalAdvantageModel(PhysicsModel):
    """Model 5: Mechanical advantage systems"""
    
    def __init__(self):
        super().__init__(
            name="mechanical_advantage",
            description="Calculate theoretical and actual mechanical advantage",
            assumptions=[
                "Ideal pulleys (frictionless)",
                "Rope does not stretch",
                "Forces are applied vertically"
            ],
            limitations=[
                "Actual MA reduced by friction (typically 50-70% of theoretical)",
                "Does not account for rope friction through pulleys",
                "Edge friction not included"
            ]
        )
    
    def compute(self, system_type, num_pulleys=2, efficiency=0.6):
        """
        Compute mechanical advantage
        system_type: 'simple', 'compound', 'complex'
        num_pulleys: number of moving pulleys
        efficiency: system efficiency (0-1)
        """
        # Theoretical MA = 2^n for simple systems with n moving pulleys
        theoretical_ma = 2 ** num_pulleys if system_type == 'simple' else num_pulleys + 1
        actual_ma = theoretical_ma * efficiency
        
        return {
            'theoretical_ma': theoretical_ma,
            'actual_ma': actual_ma,
            'efficiency': efficiency,
            'system_type': system_type
        }


class BeamDeflectionModel(PhysicsModel):
    """Model 6: Simple beam deflection"""
    
    def __init__(self):
        super().__init__(
            name="beam_deflection",
            description="Calculate deflection of a simply supported beam with center load",
            assumptions=[
                "Beam is simply supported at both ends",
                "Load is applied at center",
                "Beam material is homogeneous and isotropic",
                "Small deflections (linear elasticity)"
            ],
            limitations=[
                "Does not account for shear deformation",
                "Assumes perfect supports",
                "Material properties assumed constant"
            ]
        )
    
    def compute(self, load, span, modulus=29e6, moment_of_inertia=1):
        """
        Compute beam deflection
        load: center load in lbf
        span: beam span in feet
        modulus: Young's modulus in psi (default: steel)
        moment_of_inertia: I in in^4
        """
        # Convert span to inches
        span_inches = span * 12
        
        # Deflection = (P * L^3) / (48 * E * I)
        deflection = (load * span_inches ** 3) / (48 * modulus * moment_of_inertia)
        
        return {
            'deflection_inches': deflection,
            'load': load,
            'span_feet': span
        }


class PendulumModel(PhysicsModel):
    """Model 7: Simple pendulum period"""
    
    def __init__(self):
        super().__init__(
            name="pendulum",
            description="Calculate period of a simple pendulum",
            assumptions=[
                "Small angle oscillations (< 15°)",
                "Massless string",
                "Point mass at end",
                "No air resistance"
            ],
            limitations=[
                "Large angles require elliptic integral solution",
                "Actual rope has mass",
                "Air resistance affects period"
            ]
        )
    
    def compute(self, length):
        """
        Compute pendulum period
        length: pendulum length in feet
        """
        # Convert to meters for standard g
        length_m = Length(length, 'feet').to_meters()
        g = 9.81  # m/s^2
        
        # T = 2π√(L/g)
        period = 2 * math.pi * math.sqrt(length_m / g)
        
        return {
            'period_seconds': period,
            'length_feet': length,
            'frequency_hz': 1 / period
        }


# Model registry
MODELS = {
    'vector': VectorModel(),
    'bridle_two_leg_equal_angle': BridleTwoLegModel(),
    'highline_tension': HighlineModel(),
    'fall_impact_force': ImpactForceModel(),
    'mechanical_advantage': MechanicalAdvantageModel(),
    'beam_deflection': BeamDeflectionModel(),
    'pendulum': PendulumModel()
}


def get_model(name):
    """Get model by name"""
    return MODELS.get(name)


def list_models():
    """List all available models"""
    return list(MODELS.keys())


# Self-test
if __name__ == "__main__":
    print("TRIG6 Model Registry Self-Test")
    print("=" * 70)
    
    print(f"\nTotal models: {len(MODELS)}")
    print("\nAvailable models:")
    for name in list_models():
        print(f"  - {name}")
    
    # Test vector model
    print("\n" + "=" * 70)
    vector_model = get_model('vector')
    print(vector_model.explain())
    result = vector_model.compute(theta=45)
    print(f"\nVector at 45°:")
    for func, value in result.items():
        print(f"  {func}: {value:.6f}")
    
    # Test bridle model
    print("\n" + "=" * 70)
    bridle_model = get_model('bridle_two_leg_equal_angle')
    result = bridle_model.compute(load=300, theta=30)
    print(f"\nBridle with 300 lbf at 30°:")
    print(f"  Tension per leg: {result['tension_per_leg']:.2f} lbf")
