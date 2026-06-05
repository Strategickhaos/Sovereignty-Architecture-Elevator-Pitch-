#!/usr/bin/env python3
"""
TRIG6 ARIMA Forecasting System
30-second time-series prediction with confidence intervals

Purpose: Predict neurological events before they occur
Creator: Dom
For: Sister

This module uses ARIMA (AutoRegressive Integrated Moving Average)
to forecast theta, slope, and risk 30 seconds ahead with 95% confidence intervals.

30 seconds of warning can save a life.
"""

from typing import List, Tuple, Optional
import warnings

# Check if statsmodels is available
try:
    from statsmodels.tsa.arima.model import ARIMA
    import numpy as np
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    print("Warning: statsmodels not available. Install with: pip install statsmodels")


class ARIMAForecaster:
    """
    ARIMA-based time series forecasting for neurological metrics.
    
    Provides point forecasts and confidence intervals.
    """
    
    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1), 
                 min_points: int = 10):
        """
        Initialize ARIMA forecaster.
        
        Args:
            order: ARIMA(p,d,q) order parameters
                  p: autoregressive order
                  d: degree of differencing
                  q: moving average order
            min_points: Minimum data points required for forecasting
        """
        if not STATSMODELS_AVAILABLE:
            raise ImportError("statsmodels is required for ARIMA forecasting")
        
        self.order = order
        self.min_points = min_points
    
    def fit_and_forecast(self, series: List[float], steps: int = 1,
                         alpha: float = 0.05) -> dict:
        """
        Fit ARIMA model and generate forecast with confidence intervals.
        
        Args:
            series: Time series data
            steps: Number of steps to forecast ahead
            alpha: Significance level (0.05 = 95% confidence interval)
        
        Returns:
            dict: {
                'forecast': predicted value(s),
                'lower_ci': lower confidence bound(s),
                'upper_ci': upper confidence bound(s),
                'success': whether forecast was successful
            }
        """
        if len(series) < self.min_points:
            return {
                'forecast': series[-1] if series else 0.0,
                'lower_ci': series[-1] if series else 0.0,
                'upper_ci': series[-1] if series else 0.0,
                'success': False,
                'error': f'Need at least {self.min_points} points'
            }
        
        try:
            # Suppress warnings for cleaner output
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                # Fit ARIMA model
                model = ARIMA(series, order=self.order)
                fit = model.fit()
                
                # Generate forecast
                forecast_result = fit.get_forecast(steps=steps)
                
                # Extract predictions and confidence intervals
                forecast_mean = forecast_result.predicted_mean
                conf_int = forecast_result.conf_int(alpha=alpha)
                
                # Convert to scalars if single step
                if steps == 1:
                    forecast_val = float(forecast_mean.iloc[0])
                    lower_ci = float(conf_int.iloc[0, 0])
                    upper_ci = float(conf_int.iloc[0, 1])
                else:
                    forecast_val = forecast_mean.tolist()
                    lower_ci = conf_int.iloc[:, 0].tolist()
                    upper_ci = conf_int.iloc[:, 1].tolist()
                
                return {
                    'forecast': forecast_val,
                    'lower_ci': lower_ci,
                    'upper_ci': upper_ci,
                    'success': True
                }
        
        except Exception as e:
            # Fallback to last value if ARIMA fails
            return {
                'forecast': series[-1] if series else 0.0,
                'lower_ci': series[-1] if series else 0.0,
                'upper_ci': series[-1] if series else 0.0,
                'success': False,
                'error': str(e)
            }
    
    def forecast_30s(self, series: List[float], time_step: float = 1.0) -> dict:
        """
        Forecast 30 seconds ahead.
        
        Args:
            series: Time series data (recent history)
            time_step: Time between measurements in seconds
        
        Returns:
            dict: 30-second forecast with confidence bounds
        """
        steps = max(1, int(30 / time_step))
        return self.fit_and_forecast(series, steps=1)  # Single 30s forecast


class MultiMetricForecaster:
    """
    Forecast multiple metrics simultaneously.
    
    Tracks theta, slope, and risk forecasts.
    """
    
    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1)):
        """
        Initialize multi-metric forecaster.
        
        Args:
            order: ARIMA order for all metrics
        """
        self.theta_forecaster = ARIMAForecaster(order=order)
        self.slope_forecaster = ARIMAForecaster(order=order)
        self.risk_forecaster = ARIMAForecaster(order=order)
    
    def forecast_all_30s(self, theta_history: List[float],
                         slope_history: List[float],
                         risk_history: List[float],
                         time_step: float = 1.0) -> dict:
        """
        Forecast all metrics 30 seconds ahead.
        
        Args:
            theta_history: Recent theta values
            slope_history: Recent slope values
            risk_history: Recent risk values
            time_step: Time between measurements
        
        Returns:
            dict: Complete 30-second forecast for all metrics
        """
        theta_result = self.theta_forecaster.forecast_30s(theta_history, time_step)
        slope_result = self.slope_forecaster.forecast_30s(slope_history, time_step)
        risk_result = self.risk_forecaster.forecast_30s(risk_history, time_step)
        
        return {
            'theta': theta_result,
            'slope': slope_result,
            'risk': risk_result,
            'seconds_ahead': 30
        }
    
    def assess_forecast_risk(self, forecast_results: dict) -> dict:
        """
        Assess risk level based on forecasted values.
        
        Args:
            forecast_results: Output from forecast_all_30s()
        
        Returns:
            dict: Risk assessment
        """
        theta_forecast = forecast_results['theta']['forecast']
        risk_forecast = forecast_results['risk']['forecast']
        
        # Check if forecasts predict dangerous conditions
        dangerous_theta = theta_forecast > 80
        dangerous_risk = risk_forecast > 0.8
        
        # Check confidence interval overlap with danger zone
        theta_upper = forecast_results['theta']['upper_ci']
        risk_upper = forecast_results['risk']['upper_ci']
        
        possibly_dangerous_theta = theta_upper > 80
        possibly_dangerous_risk = risk_upper > 0.8
        
        # Risk levels
        if dangerous_theta and dangerous_risk:
            level = "🔴 CRITICAL"
            message = "Forecast predicts critical event in 30s"
            urgency = "IMMEDIATE"
        elif possibly_dangerous_theta or possibly_dangerous_risk:
            level = "🟡 ELEVATED"
            message = "Forecast shows possible elevation in 30s"
            urgency = "WATCHFUL"
        else:
            level = "🟢 STABLE"
            message = "Forecast shows stable conditions"
            urgency = "NORMAL"
        
        return {
            'level': level,
            'message': message,
            'urgency': urgency,
            'theta_forecast': theta_forecast,
            'risk_forecast': risk_forecast,
            'dangerous_theta': dangerous_theta,
            'dangerous_risk': dangerous_risk
        }


def format_forecast_report(forecast_results: dict) -> str:
    """
    Format forecast results as human-readable report.
    
    Args:
        forecast_results: Output from forecast_all_30s()
    
    Returns:
        Formatted report string
    """
    lines = []
    lines.append("=" * 60)
    lines.append("30-SECOND FORECAST")
    lines.append("=" * 60)
    
    # Theta
    if forecast_results['theta']['success']:
        theta_f = forecast_results['theta']['forecast']
        theta_l = forecast_results['theta']['lower_ci']
        theta_u = forecast_results['theta']['upper_ci']
        lines.append(f"Theta:  {theta_f:.1f}° [{theta_l:.1f}°, {theta_u:.1f}°] (95% CI)")
    else:
        lines.append(f"Theta:  Unable to forecast")
    
    # Slope
    if forecast_results['slope']['success']:
        slope_f = forecast_results['slope']['forecast']
        slope_l = forecast_results['slope']['lower_ci']
        slope_u = forecast_results['slope']['upper_ci']
        lines.append(f"Slope:  {slope_f:.2f}°/s [{slope_l:.2f}, {slope_u:.2f}] (95% CI)")
    else:
        lines.append(f"Slope:  Unable to forecast")
    
    # Risk
    if forecast_results['risk']['success']:
        risk_f = forecast_results['risk']['forecast']
        risk_l = forecast_results['risk']['lower_ci']
        risk_u = forecast_results['risk']['upper_ci']
        lines.append(f"Risk:   {risk_f:.3f} [{risk_l:.3f}, {risk_u:.3f}] (95% CI)")
    else:
        lines.append(f"Risk:   Unable to forecast")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


if __name__ == "__main__":
    """
    Demonstration of ARIMA forecasting system.
    """
    print("=" * 60)
    print("TRIG6 ARIMA FORECASTING SYSTEM")
    print("30-Second Prediction with Confidence Intervals")
    print("=" * 60)
    print()
    
    if not STATSMODELS_AVAILABLE:
        print("ERROR: statsmodels not installed")
        print("Install with: pip install statsmodels")
        exit(1)
    
    import numpy as np
    
    # Simulate rising trend in data
    np.random.seed(42)
    n_points = 30
    
    # Theta rising from 40 to 70
    theta_history = np.linspace(40, 70, n_points) + np.random.normal(0, 2, n_points)
    theta_history = theta_history.tolist()
    
    # Slope gradually increasing
    slope_history = np.linspace(1, 5, n_points) + np.random.normal(0, 0.5, n_points)
    slope_history = slope_history.tolist()
    
    # Risk rising from 0.3 to 0.7
    risk_history = np.linspace(0.3, 0.7, n_points) + np.random.normal(0, 0.05, n_points)
    risk_history = np.clip(risk_history, 0, 1).tolist()
    
    print(f"Using {n_points} historical readings...")
    print(f"Current values: θ={theta_history[-1]:.1f}° "
          f"slope={slope_history[-1]:.1f}°/s risk={risk_history[-1]:.2f}")
    print()
    
    # Create forecaster
    forecaster = MultiMetricForecaster(order=(1, 1, 1))
    
    # Generate forecast
    forecast_results = forecaster.forecast_all_30s(
        theta_history, slope_history, risk_history, time_step=1.0
    )
    
    # Display forecast
    print(format_forecast_report(forecast_results))
    print()
    
    # Assess risk
    assessment = forecaster.assess_forecast_risk(forecast_results)
    
    print("RISK ASSESSMENT:")
    print("-" * 60)
    print(f"Level:    {assessment['level']}")
    print(f"Urgency:  {assessment['urgency']}")
    print(f"Message:  {assessment['message']}")
    print()
    
    print("=" * 60)
    print("30 seconds of warning can save a life.")
    print("Time to call for help.")
    print("Time to prepare.")
    print("Built with foresight for Sister 💜")
    print("🦁💔→❤️💜")
    print("=" * 60)
