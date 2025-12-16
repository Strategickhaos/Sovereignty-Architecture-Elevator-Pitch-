//! # Feedback: PID Controller ("Pain" Avoidance)
//!
//! Implements a PID controller for system stability (placeholder for FlameLang).

use crate::error::Result;

/// A PID controller for homeostatic feedback
pub struct PIDController {
    /// Proportional gain
    kp: f64,
    /// Integral gain
    ki: f64,
    /// Derivative gain
    kd: f64,
    
    /// Previous error
    prev_error: f64,
    /// Integral accumulator
    integral: f64,
}

impl PIDController {
    /// Create a new PID controller
    pub fn new(kp: f64, ki: f64, kd: f64) -> Self {
        Self {
            kp,
            ki,
            kd,
            prev_error: 0.0,
            integral: 0.0,
        }
    }
    
    /// Update the controller with a new error value
    pub fn update(&mut self, error: f64, dt: f64) -> f64 {
        // Proportional term
        let p = self.kp * error;
        
        // Integral term
        self.integral += error * dt;
        let i = self.ki * self.integral;
        
        // Derivative term
        let derivative = (error - self.prev_error) / dt;
        let d = self.kd * derivative;
        
        self.prev_error = error;
        
        // PID output
        p + i + d
    }
    
    /// Reset the controller state
    pub fn reset(&mut self) {
        self.prev_error = 0.0;
        self.integral = 0.0;
    }
}

// Note: In the full implementation, this would be a buffer.flame file

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pid_controller_creation() {
        let controller = PIDController::new(1.0, 0.1, 0.01);
        assert_eq!(controller.kp, 1.0);
        assert_eq!(controller.ki, 0.1);
        assert_eq!(controller.kd, 0.01);
    }

    #[test]
    fn test_pid_controller_update() {
        let mut controller = PIDController::new(1.0, 0.0, 0.0);
        
        // Simple proportional-only test
        let output = controller.update(10.0, 0.1);
        assert_eq!(output, 10.0);
    }

    #[test]
    fn test_pid_controller_reset() {
        let mut controller = PIDController::new(1.0, 0.1, 0.01);
        
        controller.update(10.0, 0.1);
        controller.reset();
        
        assert_eq!(controller.prev_error, 0.0);
        assert_eq!(controller.integral, 0.0);
    }
}
