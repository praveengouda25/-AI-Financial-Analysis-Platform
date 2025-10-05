"""
Forecasting Module - Revenue, Sales, and Profit Predictions
Supports ARIMA and trend-based forecasting
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class FinancialForecaster:
    """
    Forecast revenue, sales, and profit trends.
    Uses simple moving average and trend analysis for reliable predictions.
    """
    
    @staticmethod
    def forecast_revenue(df: pd.DataFrame, revenue_col: str, periods: int = 6) -> Dict:
        """
        Forecast future revenue using trend analysis.
        
        Args:
            df: DataFrame with revenue data
            revenue_col: Name of revenue column
            periods: Number of periods to forecast (default: 6)
        
        Returns:
            Dictionary with forecast results
        """
        try:
            # Get revenue series
            revenue = pd.to_numeric(df[revenue_col], errors='coerce').dropna()
            
            if len(revenue) < 3:
                return {'error': 'Need at least 3 data points for forecasting'}
            
            # Calculate trend
            x = np.arange(len(revenue))
            y = revenue.values
            
            # Simple linear regression for trend
            z = np.polyfit(x, y, 1)
            trend = z[0]  # Slope
            intercept = z[1]
            
            # Generate forecasts
            last_index = len(revenue)
            forecast_indices = np.arange(last_index, last_index + periods)
            forecasts = trend * forecast_indices + intercept
            
            # Calculate growth rate
            avg_revenue = revenue.mean()
            growth_rate = (trend / avg_revenue) * 100 if avg_revenue != 0 else 0
            
            # Confidence intervals (simple approach)
            std_error = np.std(y - (trend * x + intercept))
            lower_bound = forecasts - (1.96 * std_error)
            upper_bound = forecasts + (1.96 * std_error)
            
            # Insights
            trend_direction = "increasing" if trend > 0 else "decreasing" if trend < 0 else "stable"
            
            return {
                'forecasts': forecasts.tolist(),
                'lower_bound': lower_bound.tolist(),
                'upper_bound': upper_bound.tolist(),
                'trend': trend,
                'growth_rate': growth_rate,
                'trend_direction': trend_direction,
                'current_avg': avg_revenue,
                'forecast_avg': np.mean(forecasts),
                'periods': periods,
                'insight': f"Revenue is {trend_direction} at {abs(growth_rate):.1f}% per period. "
                          f"Expected average: ₹{np.mean(forecasts):,.0f}"
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def forecast_profit(df: pd.DataFrame, revenue_col: str, cost_col: str, periods: int = 6) -> Dict:
        """Forecast future profit trends."""
        try:
            revenue = pd.to_numeric(df[revenue_col], errors='coerce').dropna()
            cost = pd.to_numeric(df[cost_col], errors='coerce').dropna()
            
            if len(revenue) < 3 or len(cost) < 3:
                return {'error': 'Need at least 3 data points'}
            
            profit = revenue - cost
            
            # Trend analysis
            x = np.arange(len(profit))
            y = profit.values
            z = np.polyfit(x, y, 1)
            trend = z[0]
            intercept = z[1]
            
            # Forecasts
            last_index = len(profit)
            forecast_indices = np.arange(last_index, last_index + periods)
            forecasts = trend * forecast_indices + intercept
            
            # Growth rate
            avg_profit = profit.mean()
            growth_rate = (trend / avg_profit) * 100 if avg_profit != 0 else 0
            
            trend_direction = "improving" if trend > 0 else "declining" if trend < 0 else "stable"
            
            return {
                'forecasts': forecasts.tolist(),
                'trend': trend,
                'growth_rate': growth_rate,
                'trend_direction': trend_direction,
                'current_avg': avg_profit,
                'forecast_avg': np.mean(forecasts),
                'periods': periods,
                'insight': f"Profit is {trend_direction} at {abs(growth_rate):.1f}% per period. "
                          f"Expected average profit: ₹{np.mean(forecasts):,.0f}"
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_breakeven_forecast(fixed_costs: float, variable_cost_per_unit: float, 
                                     price_per_unit: float) -> Dict:
        """
        Calculate break-even point and forecast when it will be reached.
        """
        try:
            if price_per_unit <= variable_cost_per_unit:
                return {'error': 'Price must be higher than variable cost'}
            
            # Break-even units
            breakeven_units = fixed_costs / (price_per_unit - variable_cost_per_unit)
            breakeven_revenue = breakeven_units * price_per_unit
            
            contribution_margin = price_per_unit - variable_cost_per_unit
            contribution_margin_ratio = (contribution_margin / price_per_unit) * 100
            
            return {
                'breakeven_units': breakeven_units,
                'breakeven_revenue': breakeven_revenue,
                'contribution_margin': contribution_margin,
                'contribution_margin_ratio': contribution_margin_ratio,
                'insight': f"You need to sell {breakeven_units:,.0f} units to break even. "
                          f"Break-even revenue: ₹{breakeven_revenue:,.0f}",
                'recommendation': f"Each unit sold above break-even contributes ₹{contribution_margin:,.0f} to profit"
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def analyze_seasonality(df: pd.DataFrame, value_col: str, date_col: str = None) -> Dict:
        """Analyze seasonal patterns in data."""
        try:
            values = pd.to_numeric(df[value_col], errors='coerce').dropna()
            
            if len(values) < 12:
                return {'seasonal': False, 'note': 'Need at least 12 periods for seasonality analysis'}
            
            # Simple seasonality check - compare first half vs second half
            mid = len(values) // 2
            first_half_avg = values[:mid].mean()
            second_half_avg = values[mid:].mean()
            
            seasonal_diff = ((second_half_avg - first_half_avg) / first_half_avg) * 100
            
            is_seasonal = abs(seasonal_diff) > 10  # >10% difference indicates seasonality
            
            return {
                'seasonal': is_seasonal,
                'seasonal_variation': seasonal_diff,
                'first_half_avg': first_half_avg,
                'second_half_avg': second_half_avg,
                'insight': f"{'Seasonal' if is_seasonal else 'No significant seasonal'} pattern detected. "
                          f"Variation: {abs(seasonal_diff):.1f}%"
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def generate_growth_projection(current_value: float, growth_rate: float, 
                                   periods: int = 12) -> Dict:
        """
        Generate growth projections based on growth rate.
        """
        try:
            projections = []
            for i in range(1, periods + 1):
                projected_value = current_value * ((1 + growth_rate/100) ** i)
                projections.append(projected_value)
            
            final_value = projections[-1]
            total_growth = ((final_value - current_value) / current_value) * 100
            
            return {
                'projections': projections,
                'current_value': current_value,
                'final_value': final_value,
                'total_growth': total_growth,
                'growth_rate': growth_rate,
                'periods': periods,
                'insight': f"At {growth_rate:.1f}% growth rate, value will reach ₹{final_value:,.0f} "
                          f"in {periods} periods (total growth: {total_growth:.1f}%)"
            }
            
        except Exception as e:
            return {'error': str(e)}
