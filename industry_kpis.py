"""
Industry-Specific KPIs Module
Calculates KPIs for Retail, Service, Manufacturing, and Finance industries
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


class IndustryKPIs:
    """Calculate industry-specific Key Performance Indicators."""
    
    # RETAIL INDUSTRY KPIs
    @staticmethod
    def calculate_inventory_turnover(cogs: float, avg_inventory: float) -> Dict:
        """
        Inventory Turnover Ratio for Retail.
        Formula: COGS / Average Inventory
        """
        try:
            if avg_inventory == 0:
                return {'error': 'Average inventory cannot be zero'}
            
            turnover = cogs / avg_inventory
            days_inventory = 365 / turnover if turnover > 0 else 0
            
            # Interpretation
            if turnover > 8:
                status = "Excellent - Fast moving inventory"
            elif turnover > 4:
                status = "Good - Healthy turnover"
            elif turnover > 2:
                status = "Average - Monitor closely"
            else:
                status = "Slow - Overstocking risk"
            
            return {
                'inventory_turnover': round(turnover, 2),
                'days_inventory_outstanding': round(days_inventory, 0),
                'cogs': round(cogs, 2),
                'avg_inventory': round(avg_inventory, 2),
                'status': status,
                'insight': f"Inventory turns {turnover:.1f} times per year ({days_inventory:.0f} days). {status}",
                'benchmark': 'Retail average: 4-8 times/year'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_sales_per_sqft(revenue: float, store_sqft: float) -> Dict:
        """
        Sales per Square Foot for Retail.
        Formula: Revenue / Store Square Footage
        """
        try:
            if store_sqft == 0:
                return {'error': 'Store square footage cannot be zero'}
            
            sales_per_sqft = revenue / store_sqft
            
            # Interpretation (in Rupees)
            if sales_per_sqft > 5000:
                status = "Excellent - High productivity"
            elif sales_per_sqft > 3000:
                status = "Good - Above average"
            elif sales_per_sqft > 1500:
                status = "Average - Room for improvement"
            else:
                status = "Low - Optimize space usage"
            
            return {
                'sales_per_sqft': round(sales_per_sqft, 2),
                'revenue': round(revenue, 2),
                'store_sqft': round(store_sqft, 2),
                'status': status,
                'insight': f"₹{sales_per_sqft:,.0f} per sq ft. {status}",
                'benchmark': 'Retail average: ₹2,000-₹4,000/sq ft'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_basket_value(revenue: float, num_transactions: int) -> Dict:
        """
        Average Basket Value for Retail.
        Formula: Revenue / Number of Transactions
        """
        try:
            if num_transactions == 0:
                return {'error': 'Number of transactions cannot be zero'}
            
            avg_basket = revenue / num_transactions
            
            return {
                'average_basket_value': round(avg_basket, 2),
                'revenue': round(revenue, 2),
                'num_transactions': num_transactions,
                'insight': f"Average transaction value: ₹{avg_basket:,.2f}",
                'recommendation': 'Increase basket size through upselling and cross-selling'
            }
        except Exception as e:
            return {'error': str(e)}
    
    # SERVICE INDUSTRY KPIs
    @staticmethod
    def calculate_cac(marketing_cost: float, new_customers: int) -> Dict:
        """
        Customer Acquisition Cost (CAC) for Services.
        Formula: Marketing Cost / New Customers
        """
        try:
            if new_customers == 0:
                return {'error': 'Number of new customers cannot be zero'}
            
            cac = marketing_cost / new_customers
            
            # Interpretation
            if cac < 500:
                status = "Excellent - Low acquisition cost"
            elif cac < 2000:
                status = "Good - Reasonable CAC"
            elif cac < 5000:
                status = "Moderate - Monitor efficiency"
            else:
                status = "High - Optimize marketing spend"
            
            return {
                'cac': round(cac, 2),
                'marketing_cost': round(marketing_cost, 2),
                'new_customers': new_customers,
                'status': status,
                'insight': f"Cost to acquire one customer: ₹{cac:,.2f}. {status}",
                'benchmark': 'Service industry average: ₹1,000-₹3,000'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_clv(avg_revenue_per_customer: float, avg_customer_lifespan_years: float,
                     profit_margin: float) -> Dict:
        """
        Customer Lifetime Value (CLV) for Services.
        Formula: Avg Revenue per Customer × Avg Lifespan × Profit Margin
        """
        try:
            clv = avg_revenue_per_customer * avg_customer_lifespan_years * profit_margin
            
            return {
                'clv': round(clv, 2),
                'avg_revenue_per_customer': round(avg_revenue_per_customer, 2),
                'avg_lifespan_years': avg_customer_lifespan_years,
                'profit_margin': profit_margin,
                'insight': f"Average customer lifetime value: ₹{clv:,.2f}",
                'recommendation': 'Focus on retention to maximize CLV'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_utilization_rate(billable_hours: float, total_hours: float) -> Dict:
        """
        Utilization Rate for Services.
        Formula: Billable Hours / Total Available Hours × 100
        """
        try:
            if total_hours == 0:
                return {'error': 'Total hours cannot be zero'}
            
            utilization = (billable_hours / total_hours) * 100
            
            # Interpretation
            if utilization > 85:
                status = "Excellent - High utilization"
            elif utilization > 70:
                status = "Good - Healthy utilization"
            elif utilization > 50:
                status = "Average - Room for improvement"
            else:
                status = "Low - Underutilized capacity"
            
            return {
                'utilization_rate': round(utilization, 2),
                'billable_hours': round(billable_hours, 2),
                'total_hours': round(total_hours, 2),
                'status': status,
                'insight': f"{utilization:.1f}% of time is billable. {status}",
                'benchmark': 'Service industry target: 75-85%'
            }
        except Exception as e:
            return {'error': str(e)}
    
    # MANUFACTURING INDUSTRY KPIs
    @staticmethod
    def calculate_production_efficiency(actual_output: float, theoretical_capacity: float) -> Dict:
        """
        Production Efficiency for Manufacturing.
        Formula: Actual Output / Theoretical Capacity × 100
        """
        try:
            if theoretical_capacity == 0:
                return {'error': 'Theoretical capacity cannot be zero'}
            
            efficiency = (actual_output / theoretical_capacity) * 100
            
            # Interpretation
            if efficiency > 90:
                status = "Excellent - Near maximum capacity"
            elif efficiency > 75:
                status = "Good - Efficient production"
            elif efficiency > 60:
                status = "Average - Improvement needed"
            else:
                status = "Low - Significant underutilization"
            
            return {
                'production_efficiency': round(efficiency, 2),
                'actual_output': round(actual_output, 2),
                'theoretical_capacity': round(theoretical_capacity, 2),
                'capacity_gap': round(theoretical_capacity - actual_output, 2),
                'status': status,
                'insight': f"Operating at {efficiency:.1f}% of capacity. {status}",
                'benchmark': 'Manufacturing target: 80-95%'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_cost_per_unit(total_cost: float, units_produced: float) -> Dict:
        """
        Cost per Unit for Manufacturing.
        Formula: Total Cost / Units Produced
        """
        try:
            if units_produced == 0:
                return {'error': 'Units produced cannot be zero'}
            
            cost_per_unit = total_cost / units_produced
            
            return {
                'cost_per_unit': round(cost_per_unit, 2),
                'total_cost': round(total_cost, 2),
                'units_produced': round(units_produced, 2),
                'insight': f"Cost to produce one unit: ₹{cost_per_unit:,.2f}",
                'recommendation': 'Monitor for economies of scale opportunities'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_defect_rate(defective_units: float, total_units: float) -> Dict:
        """
        Defect Rate for Manufacturing.
        Formula: Defective Units / Total Units × 100
        """
        try:
            if total_units == 0:
                return {'error': 'Total units cannot be zero'}
            
            defect_rate = (defective_units / total_units) * 100
            
            # Interpretation
            if defect_rate < 1:
                status = "Excellent - High quality"
            elif defect_rate < 3:
                status = "Good - Acceptable quality"
            elif defect_rate < 5:
                status = "Average - Quality improvement needed"
            else:
                status = "High - Critical quality issues"
            
            return {
                'defect_rate': round(defect_rate, 2),
                'defective_units': round(defective_units, 2),
                'total_units': round(total_units, 2),
                'status': status,
                'insight': f"{defect_rate:.2f}% defect rate. {status}",
                'benchmark': 'Manufacturing target: <2%'
            }
        except Exception as e:
            return {'error': str(e)}
    
    # FINANCE/INVESTMENT KPIs
    @staticmethod
    def calculate_sharpe_ratio(portfolio_return: float, risk_free_rate: float, 
                              std_deviation: float) -> Dict:
        """
        Sharpe Ratio for Investment Analysis.
        Formula: (Portfolio Return - Risk Free Rate) / Standard Deviation
        """
        try:
            if std_deviation == 0:
                return {'error': 'Standard deviation cannot be zero'}
            
            sharpe = (portfolio_return - risk_free_rate) / std_deviation
            
            # Interpretation
            if sharpe > 2:
                status = "Excellent - High risk-adjusted return"
            elif sharpe > 1:
                status = "Good - Adequate risk-adjusted return"
            elif sharpe > 0:
                status = "Moderate - Below optimal"
            else:
                status = "Poor - Not compensating for risk"
            
            return {
                'sharpe_ratio': round(sharpe, 4),
                'portfolio_return': round(portfolio_return, 4),
                'risk_free_rate': round(risk_free_rate, 4),
                'std_deviation': round(std_deviation, 4),
                'excess_return': round(portfolio_return - risk_free_rate, 4),
                'status': status,
                'insight': f"Sharpe ratio: {sharpe:.2f}. {status}",
                'benchmark': 'Good Sharpe ratio: >1.0'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_portfolio_diversification(num_assets: int, correlation_avg: float) -> Dict:
        """
        Portfolio Diversification Index.
        Lower correlation = better diversification
        """
        try:
            # Diversification score (0-100)
            # More assets and lower correlation = higher score
            asset_score = min(num_assets * 5, 50)  # Max 50 points for assets
            correlation_score = (1 - abs(correlation_avg)) * 50  # Max 50 points for low correlation
            
            diversification_index = asset_score + correlation_score
            
            # Interpretation
            if diversification_index > 80:
                status = "Excellent - Well diversified"
            elif diversification_index > 60:
                status = "Good - Adequate diversification"
            elif diversification_index > 40:
                status = "Moderate - More diversification needed"
            else:
                status = "Low - Concentration risk"
            
            return {
                'diversification_index': round(diversification_index, 2),
                'num_assets': num_assets,
                'avg_correlation': round(correlation_avg, 4),
                'status': status,
                'insight': f"Diversification score: {diversification_index:.0f}/100. {status}",
                'recommendation': 'Add uncorrelated assets to improve diversification'
            }
        except Exception as e:
            return {'error': str(e)}
