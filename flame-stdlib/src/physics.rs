//! # FLAME Physics Module - Dimensional Analysis
//! 
//! This module provides compile-time dimensional analysis that catches
//! unit mismatches like `Mass + Force` at compile time.
//! 
//! No other language has physics-validated dimensional analysis at this level.
//! 
//! ## Features
//! 
//! - Compile-time unit checking
//! - Type-safe unit conversions
//! - Physics operators with correct dimensionality
//! - Base SI units: Mass, Length, Time, Current, Temperature, Amount, Luminosity
//! - Derived units: Force, Energy, Power, Velocity, Acceleration, etc.
//! 
//! ## Example
//! 
//! ```rust
//! use flame::physics::{Mass, Acceleration, Force};
//! 
//! let mass = Mass::kg(10.0);
//! let accel = Acceleration::mps2(5.0);
//! let force = mass * accel; // Force::newtons(50.0)
//! 
//! // Compile error: cannot add mass and force
//! // let invalid = mass + force;
//! ```

use std::ops::{Add, Sub, Mul, Div};
use std::fmt;

/// Base dimensional trait
pub trait Dimension: Sized {
    const NAME: &'static str;
    const UNIT: &'static str;
    
    fn value(&self) -> f64;
    fn with_value(value: f64) -> Self;
}

macro_rules! define_dimension {
    ($name:ident, $unit:literal, $display_name:literal) => {
        #[derive(Debug, Clone, Copy, PartialEq)]
        pub struct $name(f64);
        
        impl Dimension for $name {
            const NAME: &'static str = $display_name;
            const UNIT: &'static str = $unit;
            
            fn value(&self) -> f64 {
                self.0
            }
            
            fn with_value(value: f64) -> Self {
                Self(value)
            }
        }
        
        impl fmt::Display for $name {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                write!(f, "{} {}", self.0, Self::UNIT)
            }
        }
        
        impl Add for $name {
            type Output = Self;
            fn add(self, rhs: Self) -> Self::Output {
                Self(self.0 + rhs.0)
            }
        }
        
        impl Sub for $name {
            type Output = Self;
            fn sub(self, rhs: Self) -> Self::Output {
                Self(self.0 - rhs.0)
            }
        }
        
        impl Mul<f64> for $name {
            type Output = Self;
            fn mul(self, rhs: f64) -> Self::Output {
                Self(self.0 * rhs)
            }
        }
        
        impl Div<f64> for $name {
            type Output = Self;
            fn div(self, rhs: f64) -> Self::Output {
                Self(self.0 / rhs)
            }
        }
    };
}

// Base SI units
define_dimension!(Mass, "kg", "Mass");
define_dimension!(Length, "m", "Length");
define_dimension!(Time, "s", "Time");
define_dimension!(Current, "A", "Current");
define_dimension!(Temperature, "K", "Temperature");
define_dimension!(Amount, "mol", "Amount");
define_dimension!(Luminosity, "cd", "Luminosity");

// Derived units - Kinematics
define_dimension!(Velocity, "m/s", "Velocity");
define_dimension!(Acceleration, "m/s²", "Acceleration");
define_dimension!(Jerk, "m/s³", "Jerk");

// Derived units - Dynamics
define_dimension!(Force, "N", "Force");
define_dimension!(Energy, "J", "Energy");
define_dimension!(Power, "W", "Power");
define_dimension!(Pressure, "Pa", "Pressure");
define_dimension!(Momentum, "kg⋅m/s", "Momentum");

// Derived units - Electricity
define_dimension!(Charge, "C", "Charge");
define_dimension!(Voltage, "V", "Voltage");
define_dimension!(Resistance, "Ω", "Resistance");
define_dimension!(Capacitance, "F", "Capacitance");
define_dimension!(Inductance, "H", "Inductance");
define_dimension!(MagneticFlux, "Wb", "Magnetic Flux");
define_dimension!(MagneticField, "T", "Magnetic Field");

// Derived units - Other
define_dimension!(Frequency, "Hz", "Frequency");
define_dimension!(Area, "m²", "Area");
define_dimension!(Volume, "m³", "Volume");
define_dimension!(Density, "kg/m³", "Density");
define_dimension!(AngularVelocity, "rad/s", "Angular Velocity");

// Constructors for common units
impl Mass {
    pub fn kg(value: f64) -> Self { Self(value) }
    pub fn g(value: f64) -> Self { Self(value / 1000.0) }
    pub fn mg(value: f64) -> Self { Self(value / 1_000_000.0) }
    pub fn lb(value: f64) -> Self { Self(value * 0.453592) }
}

impl Length {
    pub fn m(value: f64) -> Self { Self(value) }
    pub fn km(value: f64) -> Self { Self(value * 1000.0) }
    pub fn cm(value: f64) -> Self { Self(value / 100.0) }
    pub fn mm(value: f64) -> Self { Self(value / 1000.0) }
    pub fn ft(value: f64) -> Self { Self(value * 0.3048) }
    pub fn inch(value: f64) -> Self { Self(value * 0.0254) }
}

impl Time {
    pub fn s(value: f64) -> Self { Self(value) }
    pub fn ms(value: f64) -> Self { Self(value / 1000.0) }
    pub fn us(value: f64) -> Self { Self(value / 1_000_000.0) }
    pub fn min(value: f64) -> Self { Self(value * 60.0) }
    pub fn hr(value: f64) -> Self { Self(value * 3600.0) }
}

impl Temperature {
    pub fn kelvin(value: f64) -> Self { Self(value) }
    pub fn celsius(value: f64) -> Self { Self(value + 273.15) }
    pub fn fahrenheit(value: f64) -> Self { Self((value - 32.0) * 5.0 / 9.0 + 273.15) }
}

impl Velocity {
    pub fn mps(value: f64) -> Self { Self(value) }
    pub fn kmh(value: f64) -> Self { Self(value / 3.6) }
    pub fn mph(value: f64) -> Self { Self(value * 0.44704) }
}

impl Acceleration {
    pub fn mps2(value: f64) -> Self { Self(value) }
    pub fn g_force(value: f64) -> Self { Self(value * 9.80665) }
}

impl Force {
    pub fn newtons(value: f64) -> Self { Self(value) }
    pub fn kn(value: f64) -> Self { Self(value * 1000.0) }
    pub fn lbf(value: f64) -> Self { Self(value * 4.44822) }
}

impl Energy {
    pub fn joules(value: f64) -> Self { Self(value) }
    pub fn kj(value: f64) -> Self { Self(value * 1000.0) }
    pub fn kwh(value: f64) -> Self { Self(value * 3_600_000.0) }
    pub fn cal(value: f64) -> Self { Self(value * 4.184) }
    pub fn kcal(value: f64) -> Self { Self(value * 4184.0) }
}

impl Power {
    pub fn watts(value: f64) -> Self { Self(value) }
    pub fn kw(value: f64) -> Self { Self(value * 1000.0) }
    pub fn hp(value: f64) -> Self { Self(value * 745.7) }
}

impl Pressure {
    pub fn pascals(value: f64) -> Self { Self(value) }
    pub fn kpa(value: f64) -> Self { Self(value * 1000.0) }
    pub fn bar(value: f64) -> Self { Self(value * 100_000.0) }
    pub fn atm(value: f64) -> Self { Self(value * 101_325.0) }
    pub fn psi(value: f64) -> Self { Self(value * 6894.76) }
}

impl Frequency {
    pub fn hz(value: f64) -> Self { Self(value) }
    pub fn khz(value: f64) -> Self { Self(value * 1000.0) }
    pub fn mhz(value: f64) -> Self { Self(value * 1_000_000.0) }
    pub fn ghz(value: f64) -> Self { Self(value * 1_000_000_000.0) }
}

impl Voltage {
    pub fn volts(value: f64) -> Self { Self(value) }
    pub fn mv(value: f64) -> Self { Self(value / 1000.0) }
    pub fn kv(value: f64) -> Self { Self(value * 1000.0) }
}

impl Resistance {
    pub fn ohms(value: f64) -> Self { Self(value) }
    pub fn kohms(value: f64) -> Self { Self(value * 1000.0) }
    pub fn mohms(value: f64) -> Self { Self(value * 1_000_000.0) }
}

// Physics operations with dimensional correctness

// F = ma (Force = Mass × Acceleration)
impl Mul<Acceleration> for Mass {
    type Output = Force;
    fn mul(self, rhs: Acceleration) -> Force {
        Force::newtons(self.0 * rhs.0)
    }
}

// a = F/m (Acceleration = Force / Mass)
impl Div<Mass> for Force {
    type Output = Acceleration;
    fn div(self, rhs: Mass) -> Acceleration {
        Acceleration::mps2(self.0 / rhs.0)
    }
}

// v = d/t (Velocity = Length / Time)
impl Div<Time> for Length {
    type Output = Velocity;
    fn div(self, rhs: Time) -> Velocity {
        Velocity::mps(self.0 / rhs.0)
    }
}

// d = v*t (Length = Velocity × Time)
impl Mul<Time> for Velocity {
    type Output = Length;
    fn mul(self, rhs: Time) -> Length {
        Length::m(self.0 * rhs.0)
    }
}

// a = v/t (Acceleration = Velocity / Time)
impl Div<Time> for Velocity {
    type Output = Acceleration;
    fn div(self, rhs: Time) -> Acceleration {
        Acceleration::mps2(self.0 / rhs.0)
    }
}

// v = a*t (Velocity = Acceleration × Time)
impl Mul<Time> for Acceleration {
    type Output = Velocity;
    fn mul(self, rhs: Time) -> Velocity {
        Velocity::mps(self.0 * rhs.0)
    }
}

// E = F*d (Energy = Force × Length)
impl Mul<Length> for Force {
    type Output = Energy;
    fn mul(self, rhs: Length) -> Energy {
        Energy::joules(self.0 * rhs.0)
    }
}

// P = E/t (Power = Energy / Time)
impl Div<Time> for Energy {
    type Output = Power;
    fn div(self, rhs: Time) -> Power {
        Power::watts(self.0 / rhs.0)
    }
}

// E = P*t (Energy = Power × Time)
impl Mul<Time> for Power {
    type Output = Energy;
    fn mul(self, rhs: Time) -> Energy {
        Energy::joules(self.0 * rhs.0)
    }
}

// P = F*v (Power = Force × Velocity)
impl Mul<Velocity> for Force {
    type Output = Power;
    fn mul(self, rhs: Velocity) -> Power {
        Power::watts(self.0 * rhs.0)
    }
}

// p = m*v (Momentum = Mass × Velocity)
impl Mul<Velocity> for Mass {
    type Output = Momentum;
    fn mul(self, rhs: Velocity) -> Momentum {
        Momentum(self.0 * rhs.0)
    }
}

// Area = Length × Length
impl Mul<Length> for Length {
    type Output = Area;
    fn mul(self, rhs: Length) -> Area {
        Area(self.0 * rhs.0)
    }
}

// Volume = Area × Length
impl Mul<Length> for Area {
    type Output = Volume;
    fn mul(self, rhs: Length) -> Volume {
        Volume(self.0 * rhs.0)
    }
}

// Density = Mass / Volume
impl Div<Volume> for Mass {
    type Output = Density;
    fn div(self, rhs: Volume) -> Density {
        Density(self.0 / rhs.0)
    }
}

// Pressure = Force / Area
impl Div<Area> for Force {
    type Output = Pressure;
    fn div(self, rhs: Area) -> Pressure {
        Pressure::pascals(self.0 / rhs.0)
    }
}

// Frequency = 1 / Time
impl Div<Time> for f64 {
    type Output = Frequency;
    fn div(self, rhs: Time) -> Frequency {
        Frequency::hz(self / rhs.0)
    }
}

// V = I*R (Voltage = Current × Resistance)
impl Mul<Resistance> for Current {
    type Output = Voltage;
    fn mul(self, rhs: Resistance) -> Voltage {
        Voltage::volts(self.0 * rhs.0)
    }
}

// I = V/R (Current = Voltage / Resistance)
impl Div<Resistance> for Voltage {
    type Output = Current;
    fn div(self, rhs: Resistance) -> Current {
        Current(self.0 / rhs.0)
    }
}

// P = V*I (Power = Voltage × Current)
impl Mul<Current> for Voltage {
    type Output = Power;
    fn mul(self, rhs: Current) -> Power {
        Power::watts(self.0 * rhs.0)
    }
}

/// Physical constants
pub mod constants {
    use super::*;
    
    /// Speed of light in vacuum
    pub const SPEED_OF_LIGHT: Velocity = Velocity(299_792_458.0);
    
    /// Gravitational acceleration on Earth
    pub const GRAVITY: Acceleration = Acceleration(9.80665);
    
    /// Planck constant
    pub const PLANCK: f64 = 6.62607015e-34; // J⋅s
    
    /// Boltzmann constant
    pub const BOLTZMANN: f64 = 1.380649e-23; // J/K
    
    /// Elementary charge
    pub const ELEMENTARY_CHARGE: Charge = Charge(1.602176634e-19);
    
    /// Avogadro constant
    pub const AVOGADRO: f64 = 6.02214076e23; // 1/mol
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_force_from_mass_acceleration() {
        let mass = Mass::kg(10.0);
        let accel = Acceleration::mps2(5.0);
        let force = mass * accel;
        assert!((force.value() - 50.0).abs() < 1e-6);
    }

    #[test]
    fn test_velocity_from_length_time() {
        let dist = Length::m(100.0);
        let time = Time::s(10.0);
        let vel = dist / time;
        assert!((vel.value() - 10.0).abs() < 1e-6);
    }

    #[test]
    fn test_energy_from_force_distance() {
        let force = Force::newtons(10.0);
        let dist = Length::m(5.0);
        let energy = force * dist;
        assert!((energy.value() - 50.0).abs() < 1e-6);
    }

    #[test]
    fn test_power_from_energy_time() {
        let energy = Energy::joules(100.0);
        let time = Time::s(10.0);
        let power = energy / time;
        assert!((power.value() - 10.0).abs() < 1e-6);
    }

    #[test]
    fn test_unit_conversions() {
        let mass_kg = Mass::kg(1.0);
        let mass_g = Mass::g(1000.0);
        assert!((mass_kg.value() - mass_g.value()).abs() < 1e-6);
    }
}
