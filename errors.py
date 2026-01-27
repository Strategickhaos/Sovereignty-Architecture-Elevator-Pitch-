"""TRIG6 Error Codes and Handlers."""


class TRIG6Error(Exception):
    """Base exception for TRIG6 calculator errors."""
    pass


class SingularityError(TRIG6Error):
    """Exception raised when encountering singularities in trig functions.
    
    Error Code 6: Represents the 6 functions that can have singularities.
    """
    ERROR_CODE = 6
    
    def __init__(self, message="Division by zero at danger zone", theta=None):
        self.message = message
        self.theta = theta
        super().__init__(self.format_message())
    
    def format_message(self):
        msg = f"Singularity Error: Code {self.ERROR_CODE} - {self.message}"
        if self.theta is not None:
            msg += f" (θ = {self.theta})"
        return msg


class InvalidAngleError(TRIG6Error):
    """Exception raised for invalid angle inputs."""
    pass


# Error code constants
ERROR_CODES = {
    6: "Singularity - Division by zero in one or more trig functions",
}


def handle_singularity(func_name, theta):
    """Handle singularity errors with context."""
    print(f"Warning: Singularity detected in {func_name} at θ = {theta}")
    print("Returning infinity as appropriate.")
    return float('inf')
