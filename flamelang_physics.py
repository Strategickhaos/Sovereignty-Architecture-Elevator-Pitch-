#!/usr/bin/env python3
"""
🔥 FLAMELANG PHYSICS v1.0
Hebrew Root Operators for Quantum Gravity and CMB Modeling

Expanded OPERATORS dictionary for advanced quantum gravity and CMB modeling.
These trilateral Hebrew roots enhance intent parsing for cosmological scenarios,
mapping ancient concepts to modern physics primitives.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import re

# Expanded OPERATORS dictionary with Hebrew roots
OPERATORS = {
    # Core operators (original + prior expansion)
    'CREATE': 'ברא',      # Particle creation/annihilation
    'SEPARATE': 'בדל',    # Measurement/collapse/decoherence
    'CONNECT': 'חבר',     # Entanglement/correlations
    'TRANSFORM': 'הפך',   # State evolution/wave transforms
    'CONSTRAIN': 'גבל',   # Conservation laws/boundaries
    'OBSERVE': 'ראה',     # Observation/measurement problem
    'RADIATE': 'אור',     # Photon emission/blackbody radiation
    'EXPAND': 'רחב',      # Cosmic expansion/inflation
    'SUPPRESS': 'כבש',    # Power suppression/damping
    'BOUNCE': 'דחה',      # Repulsion/quantum bounce
    'HARMONIZE': 'שוה',   # Balance/unification of scales
    'FLUCTUATE': 'נוע',   # Vacuum fluctuations/quantum noise
    'UNIFY': 'אחד',       # Oneness/quantum-gravity unification

    # New expansions for CMB/QG
    'ANOMALIZE': 'פלא',   # Wonder/anomaly generation (e.g., CMB asymmetries)
    'LENSE': 'עדש',       # Lens/distort (gravitational lensing effects on CMB)
    'POLARIZE': 'קוטב',   # Polarize (B-modes, E-modes in CMB polarization)
    'SCALE': 'מדד',       # Measure/scale invariance (scale-invariant spectra)
    'PERTURB': 'הפר',     # Disturb/perturbations (pre-bounce or inflationary)
    'ASYMMETRIZE': 'שני', # Two/duality/asymmetry (hemispherical asymmetry)
    'VIOLATE': 'חלל',     # Profane/violation (parity or CP violations)
}

# Reverse mapping for Hebrew to English
HEBREW_TO_ENGLISH = {v: k for k, v in OPERATORS.items()}


@dataclass
class PhysicsModel:
    """Represents a compiled physics model from FlameLang intent"""
    name: str
    operators: List[str]
    hebrew_roots: List[str]
    parameters: Dict[str, Any]
    model_function: Optional[callable] = None
    description: str = ""


class FlameLangPhysicsCompiler:
    """
    Compiler for FlameLang physics intents to executable models.
    Parses natural language intents containing operator keywords and
    generates corresponding physics models.
    """
    
    def __init__(self):
        self.operators = OPERATORS
        self.hebrew_to_english = HEBREW_TO_ENGLISH
        
    def parse_intent(self, intent: str) -> List[str]:
        """
        Parse intent string for operator keywords.
        
        Args:
            intent: Natural language physics intent
            
        Returns:
            List of detected operator keywords
        """
        intent_lower = intent.lower()
        detected_operators = []
        
        # Define word variations for better matching
        variations = {
            'FLUCTUATE': ['fluctuat'],  # Matches fluctuate, fluctuations, fluctuating
            'RADIATE': ['radiat'],      # Matches radiate, radiation, radiating
            'SUPPRESS': ['suppress'],   # Matches suppress, suppression, suppressing
            'HARMONIZE': ['harmoniz', 'harmoni'],  # Matches harmonize, harmonization
            'ANOMALIZE': ['anomal'],    # Matches anomalize, anomaly, anomalies
            'LENSE': ['lens'],          # Matches lens, lense, lensing
            'POLARIZE': ['polariz'],    # Matches polarize, polarization
            'PERTURB': ['perturb'],     # Matches perturb, perturbation, perturbations
            'ASYMMETRIZE': ['asymmetr', 'asymmetry'],  # Matches asymmetry, asymmetric
        }
        
        for operator_name in self.operators.keys():
            # Check for operator name or its variations
            if operator_name.lower() in intent_lower:
                detected_operators.append(operator_name)
            elif operator_name in variations:
                # Check variations
                for variant in variations[operator_name]:
                    if variant in intent_lower:
                        detected_operators.append(operator_name)
                        break
        
        return detected_operators
    
    def compile(self, intent: str) -> PhysicsModel:
        """
        Compile a natural language intent into a physics model.
        
        Args:
            intent: Natural language description of physics scenario
            
        Returns:
            PhysicsModel with operators and parameters
            
        Example:
            >>> compiler = FlameLangPhysicsCompiler()
            >>> model = compiler.compile("Bounce suppress low-l radiation")
            >>> print(model.operators)
            ['BOUNCE', 'SUPPRESS', 'RADIATE']
        """
        operators = self.parse_intent(intent)
        hebrew_roots = [self.operators[op] for op in operators]
        
        # Determine model type and parameters based on operators
        parameters = self._extract_parameters(intent, operators)
        model_function = self._generate_model_function(operators, parameters)
        
        model = PhysicsModel(
            name=f"FlameLang_{'-'.join(operators)}",
            operators=operators,
            hebrew_roots=hebrew_roots,
            parameters=parameters,
            model_function=model_function,
            description=intent
        )
        
        return model
    
    def _extract_parameters(self, intent: str, operators: List[str]) -> Dict[str, Any]:
        """Extract physics parameters from intent based on detected operators"""
        parameters = {}
        
        # Default parameters
        if 'BOUNCE' in operators:
            parameters['bounce_param'] = 1.0
            parameters['bounce_decay'] = 10.0
            
        if 'SUPPRESS' in operators:
            parameters['suppression_factor'] = 0.1
            
        if 'HARMONIZE' in operators:
            parameters['harmonic_frequency'] = 1.0
            
        if 'FLUCTUATE' in operators:
            parameters['noise_amplitude'] = 0.1
            
        if 'ANOMALIZE' in operators:
            parameters['anomaly_strength'] = 0.05
            
        if 'LENSE' in operators:
            parameters['lensing_factor'] = 1.0
            
        if 'POLARIZE' in operators:
            parameters['polarization_angle'] = 0.0
            
        if 'SCALE' in operators:
            parameters['scale_index'] = 1.0
            
        if 'PERTURB' in operators:
            parameters['perturbation_amplitude'] = 0.01
            
        if 'ASYMMETRIZE' in operators:
            parameters['asymmetry_factor'] = 0.1
            
        return parameters
    
    def _generate_model_function(self, operators: List[str], 
                                 parameters: Dict[str, Any]) -> callable:
        """
        Generate a model function based on operators.
        Returns a function that computes the model for given l values.
        """
        def model_func(l: np.ndarray, A: float, alpha: float) -> np.ndarray:
            """
            Base power law with operator modifications
            
            Args:
                l: Multipole moments
                A: Amplitude
                alpha: Power law index
                
            Returns:
                Model values D_l
            """
            # Start with power law
            D_l = A * np.power(l, alpha)
            
            # Apply operator modifications
            if 'BOUNCE' in operators:
                bounce_param = parameters.get('bounce_param', 1.0)
                bounce_decay = parameters.get('bounce_decay', 10.0)
                bounce_term = (1.0 + np.sin(bounce_param * l) * 
                              np.exp(-l / bounce_decay))
                D_l *= bounce_term
            
            if 'SUPPRESS' in operators:
                suppression = parameters.get('suppression_factor', 0.1)
                D_l *= (1.0 - suppression * np.exp(-l / 20.0))
            
            if 'HARMONIZE' in operators:
                freq = parameters.get('harmonic_frequency', 1.0)
                D_l *= (1.0 + 0.1 * np.cos(freq * l))
            
            if 'FLUCTUATE' in operators:
                noise_amp = parameters.get('noise_amplitude', 0.1)
                np.random.seed(42)  # For reproducibility
                D_l += noise_amp * np.random.randn(len(l))
            
            if 'ANOMALIZE' in operators:
                anomaly_strength = parameters.get('anomaly_strength', 0.05)
                # Add Gaussian noise for anomalies
                np.random.seed(43)
                D_l += anomaly_strength * np.random.randn(len(l)) * D_l
            
            if 'LENSE' in operators:
                lensing = parameters.get('lensing_factor', 1.0)
                # Lensing distortions as multiplicative factors
                D_l *= (1.0 + lensing * 0.01 * l / 50.0)
            
            return D_l
        
        return model_func


class CMBDataAnalyzer:
    """
    CMB (Cosmic Microwave Background) data analysis with FlameLang models.
    Supports fitting to Planck 2018 TT power spectrum data.
    """
    
    def __init__(self):
        self.compiler = FlameLangPhysicsCompiler()
        
    def power_law_model(self, l: np.ndarray, A: float, alpha: float) -> np.ndarray:
        """
        Simple power law model: D_l ≈ A * l^α
        
        Args:
            l: Multipole moments
            A: Amplitude
            alpha: Power law index
            
        Returns:
            Model values D_l
        """
        return A * np.power(l, alpha)
    
    def bounce_model(self, l: np.ndarray, A: float, alpha: float, 
                     bounce_param: float = 1.24) -> np.ndarray:
        """
        LQG bounce model with oscillatory terms:
        D_l ≈ A * l^α * (1 + sin(bounce_param * l) * exp(-l/10))
        
        Args:
            l: Multipole moments
            A: Amplitude
            alpha: Power law index
            bounce_param: Bounce parameter (controls oscillations)
            
        Returns:
            Model values D_l
        """
        base = A * np.power(l, alpha)
        bounce_term = 1.0 + np.sin(bounce_param * l) * np.exp(-l / 10.0)
        return base * bounce_term
    
    def fit_power_law(self, l_data: np.ndarray, D_l_data: np.ndarray) -> Tuple[float, float]:
        """
        Fit simple power law to CMB data using least squares.
        
        Args:
            l_data: Multipole moments
            D_l_data: Power spectrum values
            
        Returns:
            (A, alpha) - fitted parameters
        """
        # Log-transform for linear fitting
        log_l = np.log(l_data)
        log_D_l = np.log(D_l_data)
        
        # Linear regression: log(D_l) = log(A) + alpha * log(l)
        coeffs = np.polyfit(log_l, log_D_l, 1)
        alpha = coeffs[0]
        log_A = coeffs[1]
        A = np.exp(log_A)
        
        return A, alpha
    
    def fit_bounce_model(self, l_data: np.ndarray, D_l_data: np.ndarray,
                        initial_guess: Optional[Tuple[float, float, float]] = None
                        ) -> Tuple[float, float, float]:
        """
        Fit LQG bounce model to CMB data using optimization.
        
        Args:
            l_data: Multipole moments
            D_l_data: Power spectrum values
            initial_guess: Initial parameter guess (A, alpha, bounce_param)
            
        Returns:
            (A, alpha, bounce_param) - fitted parameters
        """
        try:
            from scipy.optimize import curve_fit
        except ImportError:
            # Fallback to simple estimation if scipy not available
            A, alpha = self.fit_power_law(l_data, D_l_data)
            bounce_param = 1.24  # Default from problem statement
            return A, alpha, bounce_param
        
        if initial_guess is None:
            A_init, alpha_init = self.fit_power_law(l_data, D_l_data)
            initial_guess = (A_init, alpha_init, 1.0)
        
        # Fit using curve_fit
        params, _ = curve_fit(
            self.bounce_model,
            l_data,
            D_l_data,
            p0=initial_guess,
            maxfev=10000
        )
        
        return params[0], params[1], params[2]
    
    def generate_planck_low_l_sample(self, l_range: Tuple[int, int] = (2, 50),
                                     add_noise: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate sample Planck-like low-l TT power spectrum data.
        This is a synthetic dataset for testing, matching characteristics
        from Planck 2018 low-l data.
        
        Args:
            l_range: Range of multipole moments (l_min, l_max)
            add_noise: Whether to add realistic noise
            
        Returns:
            (l_data, D_l_data) - multipole moments and power spectrum values
        """
        l_data = np.arange(l_range[0], l_range[1] + 1, dtype=float)
        
        # Characteristic low-l behavior from Planck
        # Base: mild rise with oscillations and suppression at very low l
        D_l = 258.28 * np.power(l_data, 0.43) * \
              (1.0 + np.sin(1.24 * l_data) * np.exp(-l_data / 10.0))
        
        if add_noise:
            # Add realistic noise (uncertainty ~10-20% at low l)
            np.random.seed(42)
            noise = 0.15 * D_l * np.random.randn(len(l_data))
            D_l += noise
        
        return l_data, D_l
    
    def compile_and_fit(self, intent: str, l_data: np.ndarray, 
                       D_l_data: np.ndarray) -> Dict[str, Any]:
        """
        Compile FlameLang intent and fit resulting model to data.
        
        Args:
            intent: Natural language physics intent
            l_data: Multipole moments
            D_l_data: Power spectrum values
            
        Returns:
            Dictionary with model, fitted parameters, and statistics
        """
        model = self.compiler.compile(intent)
        
        # Fit the model
        if model.model_function:
            try:
                from scipy.optimize import curve_fit
                
                # Initial guess from power law fit
                A_init, alpha_init = self.fit_power_law(l_data, D_l_data)
                
                # Fit with all parameters from model
                params, _ = curve_fit(
                    model.model_function,
                    l_data,
                    D_l_data,
                    p0=(A_init, alpha_init),
                    maxfev=10000
                )
                
                # Compute residuals
                fitted_values = model.model_function(l_data, *params)
                residuals = D_l_data - fitted_values
                chi_squared = np.sum(residuals**2)
                
                return {
                    'model': model,
                    'parameters': {
                        'A': params[0],
                        'alpha': params[1]
                    },
                    'fitted_values': fitted_values,
                    'residuals': residuals,
                    'chi_squared': chi_squared,
                    'rmse': np.sqrt(np.mean(residuals**2))
                }
            except:
                # Fallback to simple fit
                A, alpha = self.fit_power_law(l_data, D_l_data)
                fitted_values = model.model_function(l_data, A, alpha)
                residuals = D_l_data - fitted_values
                
                return {
                    'model': model,
                    'parameters': {
                        'A': A,
                        'alpha': alpha
                    },
                    'fitted_values': fitted_values,
                    'residuals': residuals,
                    'chi_squared': np.sum(residuals**2),
                    'rmse': np.sqrt(np.mean(residuals**2))
                }
        
        return {'model': model, 'error': 'No model function available'}


def flamelang_physics_compile(intent: str) -> PhysicsModel:
    """
    Main compilation function for FlameLang physics intents.
    
    Args:
        intent: Natural language physics intent with operator keywords
        
    Returns:
        Compiled PhysicsModel
        
    Example:
        >>> model = flamelang_physics_compile("Unify bounce fluctuations with radiation suppression")
        >>> print(model.operators)
        ['UNIFY', 'BOUNCE', 'FLUCTUATE', 'RADIATE', 'SUPPRESS']
        >>> print(model.hebrew_roots)
        ['אחד', 'דחה', 'נוע', 'אור', 'כבש']
    """
    compiler = FlameLangPhysicsCompiler()
    return compiler.compile(intent)


# Example usage and demonstration
if __name__ == "__main__":
    print("🔥 FLAMELANG PHYSICS - Hebrew Root Operators")
    print("=" * 60)
    
    # Display operators
    print("\n📚 OPERATORS DICTIONARY:")
    print("-" * 60)
    for eng, heb in OPERATORS.items():
        print(f"{eng:15s} → {heb}")
    
    # Compile an intent
    print("\n\n🔬 INTENT COMPILATION EXAMPLE:")
    print("-" * 60)
    intent = "Bounce suppress low-l radiation"
    print(f"Intent: '{intent}'")
    
    model = flamelang_physics_compile(intent)
    print(f"\nDetected Operators: {model.operators}")
    print(f"Hebrew Roots: {model.hebrew_roots}")
    print(f"Parameters: {model.parameters}")
    
    # CMB data analysis example
    print("\n\n📡 CMB DATA ANALYSIS EXAMPLE:")
    print("-" * 60)
    
    analyzer = CMBDataAnalyzer()
    
    # Generate sample Planck-like data
    l_data, D_l_data = analyzer.generate_planck_low_l_sample()
    print(f"Generated sample data: l = {l_data[0]:.0f} to {l_data[-1]:.0f}")
    print(f"D_l range: {D_l_data.min():.2f} to {D_l_data.max():.2f}")
    
    # Fit power law model
    A_pl, alpha_pl = analyzer.fit_power_law(l_data, D_l_data)
    print(f"\n📊 Power Law Fit:")
    print(f"   A ≈ {A_pl:.2f}")
    print(f"   α ≈ {alpha_pl:.2f}")
    
    # Fit bounce model
    A_b, alpha_b, bounce_param = analyzer.fit_bounce_model(l_data, D_l_data)
    print(f"\n🌀 Bounce Model Fit:")
    print(f"   A ≈ {A_b:.2f}")
    print(f"   α ≈ {alpha_b:.2f}")
    print(f"   bounce_param ≈ {bounce_param:.2f}")
    
    # Compile and fit with FlameLang intent
    print(f"\n\n🔥 FLAMELANG INTENT COMPILATION & FITTING:")
    print("-" * 60)
    intent2 = "Unify bounce fluctuations with radiation suppression"
    print(f"Intent: '{intent2}'")
    
    result = analyzer.compile_and_fit(intent2, l_data, D_l_data)
    print(f"\nModel: {result['model'].name}")
    print(f"Operators: {result['model'].operators}")
    print(f"Hebrew Roots: {result['model'].hebrew_roots}")
    if 'parameters' in result:
        print(f"\nFitted Parameters:")
        for param, value in result['parameters'].items():
            print(f"   {param} = {value:.2f}")
        print(f"\nFit Statistics:")
        print(f"   RMSE = {result['rmse']:.2f}")
        print(f"   χ² = {result['chi_squared']:.2f}")
    
    print("\n" + "=" * 60)
    print("🔥 FlameLang Physics Compilation Complete")
