"""
Smart Dataset Analyzer with LLM Integration
Automatically detects dataset type and suggests relevant financial metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from datetime import datetime


class SmartFinancialAnalyzer:
    """
    Intelligent analyzer that detects dataset structure and business type,
    then automatically calculates relevant financial metrics.
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.columns = [col.lower().strip() for col in df.columns]
        self.business_type = None
        self.detected_columns = {}
        self.metrics_available = []
        
    def analyze_dataset(self) -> Dict:
        """
        Main analysis function that detects dataset type and available metrics.
        """
        # Detect column mappings
        self._detect_columns()
        
        # Detect business type
        self._detect_business_type()
        
        # Determine available metrics
        self._determine_available_metrics()
        
        return {
            'business_type': self.business_type,
            'detected_columns': self.detected_columns,
            'available_metrics': self.metrics_available,
            'data_quality': self._assess_data_quality(),
            'recommendations': self._generate_recommendations()
        }
    
    def _detect_columns(self):
        """Detect and map common financial columns."""
        column_patterns = {
            'revenue': ['revenue', 'sales', 'income', 'total_amount', 'total amount', 'sales_amount'],
            'cost': ['cost', 'expense', 'cogs', 'cost_of_goods', 'purchase', 'expenditure'],
            'profit': ['profit', 'net_income', 'earnings', 'margin'],
            'date': ['date', 'time', 'period', 'month', 'year', 'timestamp'],
            'quantity': ['quantity', 'qty', 'units', 'volume', 'count'],
            'price': ['price', 'unit_price', 'rate', 'cost_per_unit'],
            'customer': ['customer', 'client', 'buyer', 'account'],
            'product': ['product', 'item', 'sku', 'category', 'service'],
            'investment': ['investment', 'capital', 'initial', 'principal'],
            'cashflow': ['cash_flow', 'cashflow', 'cash'],
            'assets': ['assets', 'inventory', 'stock'],
            'liabilities': ['liabilities', 'debt', 'payable', 'loan'],
            'equity': ['equity', 'capital', 'owner'],
        }
        
        for key, patterns in column_patterns.items():
            for col in self.columns:
                for pattern in patterns:
                    if pattern in col:
                        # Find original column name (with proper case)
                        original_col = self.df.columns[self.columns.index(col)]
                        self.detected_columns[key] = original_col
                        break
                if key in self.detected_columns:
                    break
    
    def _detect_business_type(self):
        """Detect type of business based on columns."""
        col_set = set(self.detected_columns.keys())
        
        if {'product', 'quantity', 'assets'} & col_set:
            self.business_type = 'retail_inventory'
        elif {'customer', 'revenue', 'date'} & col_set:
            self.business_type = 'service_based'
        elif {'investment', 'cashflow'} & col_set:
            self.business_type = 'investment_portfolio'
        elif {'assets', 'liabilities', 'equity'} & col_set:
            self.business_type = 'balance_sheet'
        elif {'revenue', 'cost', 'profit'} & col_set:
            self.business_type = 'income_statement'
        else:
            self.business_type = 'general_financial'
    
    def _determine_available_metrics(self):
        """Determine which metrics can be calculated based on available data."""
        metrics = []
        
        # Basic metrics
        if 'revenue' in self.detected_columns and 'cost' in self.detected_columns:
            metrics.extend(['profit_loss_ratio', 'gross_margin', 'net_margin', 'roi'])
        
        # NPV and IRR
        if 'cashflow' in self.detected_columns or ('revenue' in self.detected_columns and 'date' in self.detected_columns):
            metrics.extend(['npv', 'irr', 'payback_period', 'profitability_index'])
        
        # Cash flow analysis
        if 'revenue' in self.detected_columns and 'cost' in self.detected_columns:
            metrics.append('cash_flow_analysis')
        
        # Break-even analysis
        if 'revenue' in self.detected_columns and 'cost' in self.detected_columns and 'quantity' in self.detected_columns:
            metrics.append('break_even_analysis')
        
        # Revenue per hour (for service businesses)
        if 'revenue' in self.detected_columns and 'date' in self.detected_columns:
            metrics.extend(['revenue_per_hour', 'sales_growth', 'revenue_forecast'])
        
        # Working capital
        if 'assets' in self.detected_columns and 'liabilities' in self.detected_columns:
            metrics.extend(['working_capital', 'current_ratio', 'quick_ratio'])
        
        # Debt-to-Equity
        if 'liabilities' in self.detected_columns and 'equity' in self.detected_columns:
            metrics.append('debt_to_equity')
        
        # Inventory turnover
        if 'cost' in self.detected_columns and 'assets' in self.detected_columns:
            metrics.append('inventory_turnover')
        
        self.metrics_available = metrics
    
    def _assess_data_quality(self) -> Dict:
        """Assess data quality and completeness."""
        return {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().sum(),
            'numeric_columns': len(self.df.select_dtypes(include=[np.number]).columns),
            'date_columns': len(self.df.select_dtypes(include=['datetime64']).columns),
            'completeness': (1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on detected data."""
        recommendations = []
        
        if self.business_type == 'retail_inventory':
            recommendations.append("📦 Detected retail/inventory dataset. Focus on inventory turnover and gross margins.")
        elif self.business_type == 'service_based':
            recommendations.append("💼 Detected service-based business. Focus on revenue per hour and customer metrics.")
        elif self.business_type == 'investment_portfolio':
            recommendations.append("💰 Detected investment data. Focus on ROI, NPV, and IRR calculations.")
        
        if 'profit_loss_ratio' in self.metrics_available:
            recommendations.append("✅ Profit/Loss analysis available - will calculate profitability metrics.")
        
        if 'npv' in self.metrics_available:
            recommendations.append("✅ Cash flow data detected - NPV and IRR calculations enabled.")
        
        if len(self.metrics_available) > 5:
            recommendations.append(f"🎯 {len(self.metrics_available)} financial metrics can be calculated automatically.")
        
        missing = []
        if 'revenue' not in self.detected_columns:
            missing.append("revenue/sales")
        if 'cost' not in self.detected_columns:
            missing.append("cost/expenses")
        if 'date' not in self.detected_columns:
            missing.append("date/time")
        
        if missing:
            recommendations.append(f"⚠️ Consider adding: {', '.join(missing)} columns for more comprehensive analysis.")
        
        return recommendations
    
    def extract_financial_data(self) -> Dict:
        """Extract and prepare financial data for calculations."""
        data = {}
        
        # Extract revenue
        if 'revenue' in self.detected_columns:
            rev_col = self.detected_columns['revenue']
            # Ensure numeric only - convert if possible
            try:
                revenue_series = pd.to_numeric(self.df[rev_col], errors='coerce').dropna()
                data['revenue'] = {
                    'total': float(revenue_series.sum()),
                    'mean': float(revenue_series.mean()),
                    'series': revenue_series.tolist()
                }
            except Exception as e:
                data['revenue'] = {
                    'total': 0,
                    'mean': 0,
                    'series': [],
                    'error': f"Could not process revenue column: {str(e)}"
                }
        
        # Extract costs
        if 'cost' in self.detected_columns:
            cost_col = self.detected_columns['cost']
            try:
                cost_series = pd.to_numeric(self.df[cost_col], errors='coerce').dropna()
                data['cost'] = {
                    'total': float(cost_series.sum()),
                    'mean': float(cost_series.mean()),
                    'series': cost_series.tolist()
                }
            except Exception as e:
                data['cost'] = {
                    'total': 0,
                    'mean': 0,
                    'series': [],
                    'error': f"Could not process cost column: {str(e)}"
                }
        
        # Calculate profit if both revenue and cost exist
        if 'revenue' in data and 'cost' in data:
            data['profit'] = {
                'total': data['revenue']['total'] - data['cost']['total'],
                'margin': ((data['revenue']['total'] - data['cost']['total']) / data['revenue']['total']) * 100 if data['revenue']['total'] > 0 else 0
            }
        
        # Extract investment data
        if 'investment' in self.detected_columns:
            inv_col = self.detected_columns['investment']
            try:
                investment_series = pd.to_numeric(self.df[inv_col], errors='coerce').dropna()
                data['investment'] = float(investment_series.sum())
            except:
                data['investment'] = 0
        
        # Extract cash flows
        if 'cashflow' in self.detected_columns:
            cf_col = self.detected_columns['cashflow']
            try:
                cashflow_series = pd.to_numeric(self.df[cf_col], errors='coerce').dropna()
                data['cashflows'] = cashflow_series.tolist()
            except:
                data['cashflows'] = []
        elif 'revenue' in data and 'cost' in data and 'error' not in data['revenue'] and 'error' not in data['cost']:
            # Generate cash flows from revenue and cost
            try:
                min_len = min(len(data['revenue']['series']), len(data['cost']['series']))
                data['cashflows'] = [
                    data['revenue']['series'][i] - data['cost']['series'][i] 
                    for i in range(min_len)
                ]
            except:
                data['cashflows'] = []
        
        # Extract time series data
        if 'date' in self.detected_columns:
            date_col = self.detected_columns['date']
            try:
                data['dates'] = pd.to_datetime(self.df[date_col])
            except:
                data['dates'] = None
        
        # Extract assets and liabilities
        if 'assets' in self.detected_columns:
            try:
                assets_series = pd.to_numeric(self.df[self.detected_columns['assets']], errors='coerce').dropna()
                data['assets'] = float(assets_series.sum())
            except:
                data['assets'] = 0
        
        if 'liabilities' in self.detected_columns:
            try:
                liabilities_series = pd.to_numeric(self.df[self.detected_columns['liabilities']], errors='coerce').dropna()
                data['liabilities'] = float(liabilities_series.sum())
            except:
                data['liabilities'] = 0
        
        if 'equity' in self.detected_columns:
            try:
                equity_series = pd.to_numeric(self.df[self.detected_columns['equity']], errors='coerce').dropna()
                data['equity'] = float(equity_series.sum())
            except:
                data['equity'] = 0
        
        # Extract quantity data
        if 'quantity' in self.detected_columns:
            qty_col = self.detected_columns['quantity']
            try:
                qty_series = pd.to_numeric(self.df[qty_col], errors='coerce').dropna()
                data['quantity'] = {
                    'total': float(qty_series.sum()),
                    'mean': float(qty_series.mean())
                }
            except:
                data['quantity'] = {'total': 0, 'mean': 0}
        
        return data
    
    def generate_llm_prompt(self) -> str:
        """Generate a prompt for LLM analysis."""
        prompt = f"""
Analyze this financial dataset:

Business Type: {self.business_type}
Total Records: {len(self.df)}
Columns Detected: {', '.join(self.detected_columns.keys())}

Dataset Preview:
{self.df.head(10).to_string()}

Summary Statistics:
{self.df.describe().to_string()}

Available Metrics: {', '.join(self.metrics_available)}

Please provide:
1. Key insights about this financial data
2. Anomalies or concerning patterns
3. Recommendations for business improvement
4. Additional metrics that should be tracked
5. Risk assessment and opportunities
"""
        return prompt


def auto_detect_and_calculate(df: pd.DataFrame) -> Dict:
    """
    Main function to automatically detect dataset type and calculate metrics.
    """
    analyzer = SmartFinancialAnalyzer(df)
    analysis_result = analyzer.analyze_dataset()
    financial_data = analyzer.extract_financial_data()
    
    return {
        'analysis': analysis_result,
        'financial_data': financial_data,
        'llm_prompt': analyzer.generate_llm_prompt()
    }
