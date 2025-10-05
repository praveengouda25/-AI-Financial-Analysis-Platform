"""
Advanced Financial Calculator
Comprehensive financial metrics for any business type
Fixed NPV, IRR, and added profit/loss ratio calculations
"""

import numpy as np
from typing import Dict, List, Union, Optional
from scipy.optimize import fsolve


class AdvancedFinancialCalculator:
    """
    Comprehensive calculator for all financial metrics.
    Handles multiple business types automatically.
    """
    
    @staticmethod
    def calculate_profit_loss_ratio(revenue: float, cost: float) -> Dict:
        """
        Calculate Profit/Loss Ratio and related metrics.
        """
        try:
            profit = revenue - cost
            profit_loss_ratio = profit / revenue if revenue > 0 else 0
            
            return {
                'profit': round(profit, 4),
                'revenue': round(revenue, 4),
                'cost': round(cost, 4),
                'profit_loss_ratio': round(profit_loss_ratio, 4),
                'profit_percentage': round(profit_loss_ratio * 100, 2),
                'is_profitable': profit > 0,
                'status': 'Profitable' if profit > 0 else 'Loss',
                'interpretation': f"{'Profit' if profit > 0 else 'Loss'} of {abs(profit):,.2f} ({abs(profit_loss_ratio)*100:.2f}%)",
                'formula': 'Profit/Loss Ratio = (Revenue - Cost) / Revenue'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_npv_fixed(cashflows: List[float], discount_rate: float) -> Dict:
        """
        Calculate NPV (Net Present Value) - FIXED VERSION.
        Handles any list of cash flows correctly.
        """
        try:
            if not cashflows or len(cashflows) == 0:
                return {'error': 'No cash flows provided'}
            
            # Calculate NPV
            npv = 0
            for t, cf in enumerate(cashflows):
                npv += cf / ((1 + discount_rate) ** t)
            
            # Calculate present values for each period
            present_values = [cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cashflows)]
            
            return {
                'npv': round(npv, 4),
                'discount_rate': round(discount_rate, 4),
                'periods': len(cashflows),
                'total_cashflow': round(sum(cashflows), 4),
                'present_values': [round(pv, 4) for pv in present_values],
                'decision': 'Accept Project' if npv > 0 else 'Reject Project',
                'interpretation': f"NPV of {npv:,.4f} indicates project {'adds' if npv > 0 else 'destroys'} value",
                'formula': 'NPV = Σ [CFt / (1 + r)^t]'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_irr_fixed(cashflows: List[float], guess: float = 0.1) -> Dict:
        """
        Calculate IRR (Internal Rate of Return) - FIXED VERSION.
        Uses numerical methods for accurate calculation.
        """
        try:
            if not cashflows or len(cashflows) < 2:
                return {'error': 'At least 2 cash flows required'}
            
            # Define NPV function for IRR calculation
            def npv_func(rate):
                return sum([cf / ((1 + rate) ** t) for t, cf in enumerate(cashflows)])
            
            # Solve for IRR
            try:
                irr = fsolve(npv_func, guess)[0]
            except:
                # Fallback to numpy if scipy fails
                try:
                    irr = np.irr(cashflows)
                except:
                    return {'error': 'Could not calculate IRR - cash flows may be invalid'}
            
            return {
                'irr': round(irr, 4),
                'irr_percentage': round(irr * 100, 2),
                'periods': len(cashflows),
                'total_cashflow': round(sum(cashflows), 4),
                'interpretation': f"IRR of {irr*100:.2f}% indicates {'good' if irr > 0.1 else 'poor'} return",
                'recommendation': 'Invest' if irr > 0.1 else 'Reconsider',
                'formula': 'IRR: Rate where NPV = 0'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_roi(total_revenue: float, total_cost: float, investment: float) -> Dict:
        """Calculate Return on Investment."""
        try:
            net_profit = total_revenue - total_cost
            roi = (net_profit / investment) if investment > 0 else 0
            
            return {
                'roi': round(roi, 4),
                'roi_percentage': round(roi * 100, 2),
                'net_profit': round(net_profit, 4),
                'investment': round(investment, 4),
                'interpretation': f"ROI of {roi*100:.2f}% on investment of {investment:,.2f}",
                'formula': 'ROI = (Revenue - Cost) / Investment'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_break_even(fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float) -> Dict:
        """Calculate Break-Even Analysis."""
        try:
            contribution_margin = price_per_unit - variable_cost_per_unit
            break_even_units = fixed_costs / contribution_margin if contribution_margin > 0 else 0
            break_even_revenue = break_even_units * price_per_unit
            
            return {
                'break_even_units': round(break_even_units, 2),
                'break_even_revenue': round(break_even_revenue, 2),
                'contribution_margin': round(contribution_margin, 4),
                'contribution_margin_ratio': round(contribution_margin / price_per_unit, 4) if price_per_unit > 0 else 0,
                'interpretation': f"Need to sell {break_even_units:.0f} units to break even",
                'formula': 'Break-Even = Fixed Costs / (Price - Variable Cost)'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_gross_margin(revenue: float, cogs: float) -> Dict:
        """Calculate Gross Margin."""
        try:
            gross_profit = revenue - cogs
            gross_margin = (gross_profit / revenue) if revenue > 0 else 0
            
            return {
                'gross_profit': round(gross_profit, 4),
                'gross_margin': round(gross_margin, 4),
                'gross_margin_percentage': round(gross_margin * 100, 2),
                'interpretation': f"Gross margin of {gross_margin*100:.2f}% indicates {'healthy' if gross_margin > 0.3 else 'low'} profitability",
                'formula': 'Gross Margin = (Revenue - COGS) / Revenue'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_net_margin(revenue: float, total_costs: float) -> Dict:
        """Calculate Net Profit Margin."""
        try:
            net_profit = revenue - total_costs
            net_margin = (net_profit / revenue) if revenue > 0 else 0
            
            return {
                'net_profit': round(net_profit, 4),
                'net_margin': round(net_margin, 4),
                'net_margin_percentage': round(net_margin * 100, 2),
                'interpretation': f"Net margin of {net_margin*100:.2f}% shows overall profitability",
                'formula': 'Net Margin = (Revenue - Total Costs) / Revenue'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_working_capital(current_assets: float, current_liabilities: float) -> Dict:
        """Calculate Working Capital metrics."""
        try:
            working_capital = current_assets - current_liabilities
            current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
            
            return {
                'working_capital': round(working_capital, 4),
                'current_ratio': round(current_ratio, 4),
                'current_assets': round(current_assets, 4),
                'current_liabilities': round(current_liabilities, 4),
                'liquidity_status': 'Healthy' if current_ratio > 1.5 else 'Adequate' if current_ratio > 1 else 'Concerning',
                'interpretation': f"Working capital of {working_capital:,.2f} with current ratio of {current_ratio:.2f}",
                'formula': 'Working Capital = Current Assets - Current Liabilities'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_debt_to_equity(total_debt: float, total_equity: float) -> Dict:
        """Calculate Debt-to-Equity Ratio."""
        try:
            de_ratio = total_debt / total_equity if total_equity > 0 else 0
            
            return {
                'debt_to_equity': round(de_ratio, 4),
                'total_debt': round(total_debt, 4),
                'total_equity': round(total_equity, 4),
                'leverage': 'High' if de_ratio > 2 else 'Moderate' if de_ratio > 1 else 'Conservative',
                'interpretation': f"D/E ratio of {de_ratio:.2f} indicates {'high' if de_ratio > 2 else 'moderate' if de_ratio > 1 else 'low'} leverage",
                'formula': 'D/E Ratio = Total Debt / Total Equity'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_inventory_turnover(cogs: float, average_inventory: float) -> Dict:
        """Calculate Inventory Turnover."""
        try:
            turnover = cogs / average_inventory if average_inventory > 0 else 0
            days_inventory = 365 / turnover if turnover > 0 else 0
            
            return {
                'inventory_turnover': round(turnover, 4),
                'days_inventory_outstanding': round(days_inventory, 2),
                'cogs': round(cogs, 4),
                'average_inventory': round(average_inventory, 4),
                'efficiency': 'Excellent' if turnover > 10 else 'Good' if turnover > 5 else 'Needs Improvement',
                'interpretation': f"Inventory turns over {turnover:.2f} times per year ({days_inventory:.0f} days)",
                'formula': 'Inventory Turnover = COGS / Average Inventory'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_revenue_per_hour(total_revenue: float, total_hours: float) -> Dict:
        """Calculate Revenue per Hour (for service businesses)."""
        try:
            rph = total_revenue / total_hours if total_hours > 0 else 0
            
            return {
                'revenue_per_hour': round(rph, 4),
                'total_revenue': round(total_revenue, 4),
                'total_hours': round(total_hours, 2),
                'daily_revenue': round(rph * 8, 2),
                'monthly_revenue': round(rph * 160, 2),
                'interpretation': f"Generating {rph:,.2f} per hour",
                'formula': 'Revenue per Hour = Total Revenue / Total Hours'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_sales_growth(current_sales: float, previous_sales: float) -> Dict:
        """Calculate Sales Growth Rate."""
        try:
            growth = ((current_sales - previous_sales) / previous_sales) if previous_sales > 0 else 0
            
            return {
                'sales_growth': round(growth, 4),
                'sales_growth_percentage': round(growth * 100, 2),
                'current_sales': round(current_sales, 4),
                'previous_sales': round(previous_sales, 4),
                'trend': 'Growing' if growth > 0 else 'Declining',
                'interpretation': f"Sales {'grew' if growth > 0 else 'declined'} by {abs(growth)*100:.2f}%",
                'formula': 'Sales Growth = (Current - Previous) / Previous'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_payback_period(initial_investment: float, annual_cashflow: float) -> Dict:
        """Calculate Payback Period."""
        try:
            payback = initial_investment / annual_cashflow if annual_cashflow > 0 else 0
            
            return {
                'payback_period_years': round(payback, 2),
                'payback_period_months': round(payback * 12, 1),
                'initial_investment': round(initial_investment, 4),
                'annual_cashflow': round(annual_cashflow, 4),
                'attractiveness': 'Attractive' if payback < 3 else 'Acceptable' if payback < 5 else 'Risky',
                'interpretation': f"Investment pays back in {payback:.2f} years",
                'formula': 'Payback Period = Initial Investment / Annual Cash Flow'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_profitability_index(npv: float, initial_investment: float) -> Dict:
        """Calculate Profitability Index."""
        try:
            pv_future_cashflows = npv + initial_investment
            pi = pv_future_cashflows / initial_investment if initial_investment > 0 else 0
            
            return {
                'profitability_index': round(pi, 4),
                'npv': round(npv, 4),
                'initial_investment': round(initial_investment, 4),
                'decision': 'Accept' if pi > 1 else 'Reject',
                'interpretation': f"PI of {pi:.2f} indicates project {'creates' if pi > 1 else 'destroys'} value",
                'formula': 'PI = (NPV + Initial Investment) / Initial Investment'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_cash_flow_analysis(revenue: float, expenses: float, initial_cash: float = 0) -> Dict:
        """Calculate comprehensive Cash Flow Analysis."""
        try:
            net_cashflow = revenue - expenses
            ending_cash = initial_cash + net_cashflow
            cashflow_margin = (net_cashflow / revenue) if revenue > 0 else 0
            
            return {
                'net_cashflow': round(net_cashflow, 4),
                'initial_cash': round(initial_cash, 4),
                'ending_cash': round(ending_cash, 4),
                'cashflow_margin': round(cashflow_margin, 4),
                'cashflow_margin_percentage': round(cashflow_margin * 100, 2),
                'status': 'Positive' if net_cashflow > 0 else 'Negative',
                'interpretation': f"{'Positive' if net_cashflow > 0 else 'Negative'} cash flow of {abs(net_cashflow):,.2f}",
                'formula': 'Net Cash Flow = Revenue - Expenses'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_all_metrics(financial_data: Dict) -> Dict:
        """
        Calculate all applicable metrics based on available data.
        Automatically selects and calculates relevant metrics.
        """
        results = {}
        
        # Profit/Loss Ratio
        if 'revenue' in financial_data and 'cost' in financial_data:
            results['profit_loss'] = AdvancedFinancialCalculator.calculate_profit_loss_ratio(
                financial_data['revenue']['total'],
                financial_data['cost']['total']
            )
        
        # ROI
        if 'revenue' in financial_data and 'cost' in financial_data and 'investment' in financial_data:
            results['roi'] = AdvancedFinancialCalculator.calculate_roi(
                financial_data['revenue']['total'],
                financial_data['cost']['total'],
                financial_data['investment']
            )
        
        # NPV and IRR
        if 'cashflows' in financial_data:
            results['npv'] = AdvancedFinancialCalculator.calculate_npv_fixed(
                financial_data['cashflows'],
                0.10  # Default 10% discount rate
            )
            results['irr'] = AdvancedFinancialCalculator.calculate_irr_fixed(
                financial_data['cashflows']
            )
        
        # Margins
        if 'revenue' in financial_data and 'cost' in financial_data:
            results['gross_margin'] = AdvancedFinancialCalculator.calculate_gross_margin(
                financial_data['revenue']['total'],
                financial_data['cost']['total']
            )
            results['net_margin'] = AdvancedFinancialCalculator.calculate_net_margin(
                financial_data['revenue']['total'],
                financial_data['cost']['total']
            )
        
        # Working Capital
        if 'assets' in financial_data and 'liabilities' in financial_data:
            results['working_capital'] = AdvancedFinancialCalculator.calculate_working_capital(
                financial_data['assets'],
                financial_data['liabilities']
            )
        
        # Debt-to-Equity
        if 'liabilities' in financial_data and 'equity' in financial_data:
            results['debt_to_equity'] = AdvancedFinancialCalculator.calculate_debt_to_equity(
                financial_data['liabilities'],
                financial_data['equity']
            )
        
        # Inventory Turnover
        if 'cost' in financial_data and 'assets' in financial_data:
            results['inventory_turnover'] = AdvancedFinancialCalculator.calculate_inventory_turnover(
                financial_data['cost']['total'],
                financial_data['assets']
            )
        
        # Cash Flow Analysis
        if 'revenue' in financial_data and 'cost' in financial_data:
            results['cashflow_analysis'] = AdvancedFinancialCalculator.calculate_cash_flow_analysis(
                financial_data['revenue']['total'],
                financial_data['cost']['total']
            )
        
        # WACC (Weighted Average Cost of Capital)
        if 'equity' in financial_data and 'liabilities' in financial_data:
            # Ensure we have valid numeric values
            equity_val = financial_data.get('equity', 0)
            debt_val = financial_data.get('liabilities', 0)
            
            if equity_val > 0 and debt_val > 0:
                results['wacc'] = AdvancedFinancialCalculator.calculate_wacc(
                    equity=equity_val,
                    debt=debt_val,
                    cost_of_equity=0.12,  # Default 12%
                    cost_of_debt=0.06,    # Default 6%
                    tax_rate=0.30         # Default 30%
                )
            else:
                results['wacc'] = {'error': 'Need positive Equity and Liabilities/Debt values for WACC calculation'}
        
        # EBITDA
        if 'revenue' in financial_data and 'cost' in financial_data:
            results['ebitda'] = AdvancedFinancialCalculator.calculate_ebitda(
                revenue=financial_data['revenue']['total'],
                operating_expenses=financial_data['cost']['total']
            )
        
        return results
    
    @staticmethod
    def calculate_wacc(equity: float, debt: float, cost_of_equity: float, 
                       cost_of_debt: float, tax_rate: float) -> Dict:
        """
        Calculate WACC (Weighted Average Cost of Capital).
        
        Formula: WACC = (E/V × Re) + (D/V × Rd × (1 - T))
        Where:
        - E = Market value of equity
        - D = Market value of debt
        - V = E + D (Total capital)
        - Re = Cost of equity
        - Rd = Cost of debt
        - T = Tax rate
        """
        try:
            total_capital = equity + debt
            
            if total_capital == 0:
                return {'error': 'Total capital (Equity + Debt) is zero'}
            
            equity_weight = equity / total_capital
            debt_weight = debt / total_capital
            
            # WACC calculation
            wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
            
            interpretation = ""
            if wacc < 0.08:
                interpretation = "Low cost of capital - favorable for investments"
            elif wacc < 0.12:
                interpretation = "Moderate cost of capital - typical range"
            else:
                interpretation = "High cost of capital - projects need higher returns"
            
            return {
                'wacc': round(wacc, 4),
                'wacc_percentage': round(wacc * 100, 2),
                'equity': round(equity, 2),
                'debt': round(debt, 2),
                'total_capital': round(total_capital, 2),
                'equity_weight': round(equity_weight, 4),
                'debt_weight': round(debt_weight, 4),
                'cost_of_equity': round(cost_of_equity, 4),
                'cost_of_debt': round(cost_of_debt, 4),
                'tax_rate': round(tax_rate, 4),
                'after_tax_cost_of_debt': round(cost_of_debt * (1 - tax_rate), 4),
                'interpretation': interpretation,
                'formula': 'WACC = (E/V × Re) + (D/V × Rd × (1 - T))',
                'recommendation': 'Use WACC as discount rate for NPV calculations'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_ebitda(revenue: float, operating_expenses: float, 
                         depreciation: float = 0, amortization: float = 0) -> Dict:
        """
        Calculate EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization).
        
        Formula: EBITDA = Revenue - Operating Expenses + Depreciation + Amortization
        """
        try:
            ebitda = revenue - operating_expenses + depreciation + amortization
            ebitda_margin = (ebitda / revenue * 100) if revenue > 0 else 0
            
            interpretation = ""
            if ebitda_margin > 20:
                interpretation = "Strong operational profitability"
            elif ebitda_margin > 10:
                interpretation = "Healthy EBITDA margin"
            elif ebitda_margin > 0:
                interpretation = "Positive but low EBITDA margin"
            else:
                interpretation = "Negative EBITDA - operational losses"
            
            return {
                'ebitda': round(ebitda, 2),
                'revenue': round(revenue, 2),
                'operating_expenses': round(operating_expenses, 2),
                'depreciation': round(depreciation, 2),
                'amortization': round(amortization, 2),
                'ebitda_margin': round(ebitda_margin, 2),
                'interpretation': interpretation,
                'formula': 'EBITDA = Revenue - Operating Expenses + D&A',
                'status': 'Positive' if ebitda > 0 else 'Negative'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_operating_cash_flow_ratio(operating_cashflow: float, 
                                           current_liabilities: float) -> Dict:
        """
        Calculate Operating Cash Flow Ratio.
        
        Formula: Operating Cash Flow Ratio = Operating Cash Flow / Current Liabilities
        """
        try:
            if current_liabilities == 0:
                return {'error': 'Current liabilities cannot be zero'}
            
            ratio = operating_cashflow / current_liabilities
            
            interpretation = ""
            if ratio > 1:
                interpretation = "Strong - can cover current liabilities with operating cash flow"
            elif ratio > 0.5:
                interpretation = "Adequate - reasonable cash flow coverage"
            else:
                interpretation = "Weak - may struggle to meet current obligations"
            
            return {
                'operating_cashflow_ratio': round(ratio, 4),
                'operating_cashflow': round(operating_cashflow, 2),
                'current_liabilities': round(current_liabilities, 2),
                'interpretation': interpretation,
                'formula': 'OCF Ratio = Operating Cash Flow / Current Liabilities',
                'benchmark': 'Ratio > 1 is considered healthy'
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def calculate_asset_turnover(revenue: float, total_assets: float) -> Dict:
        """
        Calculate Asset Turnover Ratio.
        
        Formula: Asset Turnover = Revenue / Total Assets
        """
        try:
            if total_assets == 0:
                return {'error': 'Total assets cannot be zero'}
            
            ratio = revenue / total_assets
            
            interpretation = ""
            if ratio > 2:
                interpretation = "Excellent - highly efficient asset utilization"
            elif ratio > 1:
                interpretation = "Good - efficient use of assets"
            elif ratio > 0.5:
                interpretation = "Moderate - average asset efficiency"
            else:
                interpretation = "Low - underutilizing assets"
            
            return {
                'asset_turnover': round(ratio, 4),
                'revenue': round(revenue, 2),
                'total_assets': round(total_assets, 2),
                'interpretation': interpretation,
                'formula': 'Asset Turnover = Revenue / Total Assets',
                'benchmark': 'Higher ratio indicates better asset efficiency'
            }
        except Exception as e:
            return {'error': str(e)}
