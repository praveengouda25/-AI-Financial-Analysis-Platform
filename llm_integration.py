"""
LLM Integration for AI-Powered Financial Analysis
Provides intelligent insights, recommendations, and anomaly detection
"""

import os
from typing import Dict, List, Optional
import json


class LLMFinancialAnalyzer:
    """
    Integrates with LLM (OpenAI, Anthropic, or local models) for intelligent analysis.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.use_llm = bool(self.api_key)
    
    def analyze_dataset(self, dataset_info: Dict, financial_data: Dict, metrics_results: Dict) -> Dict:
        """
        Main analysis function that generates insights using LLM.
        """
        if not self.use_llm:
            return self._generate_rule_based_insights(dataset_info, financial_data, metrics_results)
        
        try:
            # Use OpenAI API
            import openai
            openai.api_key = self.api_key
            
            prompt = self._create_analysis_prompt(dataset_info, financial_data, metrics_results)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst providing insights on business data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            
            return {
                'insights': self._parse_llm_response(analysis_text),
                'raw_analysis': analysis_text,
                'model_used': self.model,
                'source': 'llm'
            }
        
        except Exception as e:
            # Fallback to rule-based if LLM fails
            return self._generate_rule_based_insights(dataset_info, financial_data, metrics_results)
    
    def _create_analysis_prompt(self, dataset_info: Dict, financial_data: Dict, metrics_results: Dict) -> str:
        """Create a comprehensive prompt for LLM analysis."""
        prompt = f"""
Analyze the following financial dataset and provide actionable insights:

## Dataset Information
Business Type: {dataset_info.get('business_type', 'Unknown')}
Total Records: {dataset_info.get('data_quality', {}).get('total_rows', 0)}
Completeness: {dataset_info.get('data_quality', {}).get('completeness', 0):.1f}%

## Financial Summary
"""
        
        if 'revenue' in financial_data:
            prompt += f"Total Revenue: ${financial_data['revenue']['total']:,.2f}\n"
        if 'cost' in financial_data:
            prompt += f"Total Costs: ${financial_data['cost']['total']:,.2f}\n"
        if 'profit' in financial_data:
            prompt += f"Net Profit: ${financial_data['profit']['total']:,.2f} ({financial_data['profit']['margin']:.2f}%)\n"
        
        prompt += "\n## Calculated Metrics\n"
        
        for metric_name, metric_data in metrics_results.items():
            if isinstance(metric_data, dict) and 'error' not in metric_data:
                prompt += f"- {metric_name.replace('_', ' ').title()}: "
                if 'interpretation' in metric_data:
                    prompt += metric_data['interpretation'] + "\n"
                else:
                    prompt += str(metric_data) + "\n"
        
        prompt += """

Please provide:
1. **Key Insights**: 3-5 most important findings from this data
2. **Strengths**: What the business is doing well
3. **Concerns**: Areas that need attention or improvement
4. **Recommendations**: Specific actionable steps to improve financial performance
5. **Anomalies**: Any unusual patterns or outliers detected
6. **Risk Assessment**: Potential financial risks
7. **Growth Opportunities**: Areas for potential expansion or improvement

Format your response in clear sections.
"""
        
        return prompt
    
    def _parse_llm_response(self, response_text: str) -> Dict:
        """Parse LLM response into structured format."""
        sections = {
            'key_insights': [],
            'strengths': [],
            'concerns': [],
            'recommendations': [],
            'anomalies': [],
            'risks': [],
            'opportunities': []
        }
        
        # Simple parsing - split by sections
        current_section = None
        for line in response_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if 'key insight' in line.lower():
                current_section = 'key_insights'
            elif 'strength' in line.lower():
                current_section = 'strengths'
            elif 'concern' in line.lower():
                current_section = 'concerns'
            elif 'recommendation' in line.lower():
                current_section = 'recommendations'
            elif 'anomal' in line.lower():
                current_section = 'anomalies'
            elif 'risk' in line.lower():
                current_section = 'risks'
            elif 'opportunit' in line.lower() or 'growth' in line.lower():
                current_section = 'opportunities'
            elif current_section and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                sections[current_section].append(line.lstrip('- •0123456789.').strip())
        
        return sections
    
    def _generate_rule_based_insights(self, dataset_info: Dict, financial_data: Dict, metrics_results: Dict) -> Dict:
        """
        Generate insights using rule-based logic (fallback when LLM unavailable).
        """
        insights = {
            'key_insights': [],
            'strengths': [],
            'concerns': [],
            'recommendations': [],
            'anomalies': [],
            'risks': [],
            'opportunities': [],
            'source': 'rule_based'
        }
        
        # Analyze profitability
        if 'profit_loss' in metrics_results:
            pl = metrics_results['profit_loss']
            if pl.get('is_profitable'):
                insights['strengths'].append(f"Profitable operations with {pl['profit_percentage']:.2f}% profit margin")
                insights['key_insights'].append(f"Business is generating profit of ${pl['profit']:,.2f}")
            else:
                insights['concerns'].append(f"Operating at a loss of ${abs(pl['profit']):,.2f}")
                insights['recommendations'].append("Focus on reducing costs or increasing revenue to achieve profitability")
        
        # Analyze margins
        if 'gross_margin' in metrics_results:
            gm = metrics_results['gross_margin']
            if gm['gross_margin_percentage'] > 30:
                insights['strengths'].append(f"Strong gross margin of {gm['gross_margin_percentage']:.2f}%")
            elif gm['gross_margin_percentage'] < 20:
                insights['concerns'].append(f"Low gross margin of {gm['gross_margin_percentage']:.2f}%")
                insights['recommendations'].append("Consider increasing prices or reducing cost of goods sold")
        
        # Analyze ROI
        if 'roi' in metrics_results:
            roi = metrics_results['roi']
            if roi['roi_percentage'] > 20:
                insights['key_insights'].append(f"Excellent ROI of {roi['roi_percentage']:.2f}%")
                insights['strengths'].append("Investment is generating strong returns")
            elif roi['roi_percentage'] < 0:
                insights['concerns'].append(f"Negative ROI of {roi['roi_percentage']:.2f}%")
                insights['recommendations'].append("Re-evaluate investment strategy and cost structure")
        
        # Analyze NPV
        if 'npv' in metrics_results:
            npv = metrics_results['npv']
            if npv.get('npv', 0) > 0:
                insights['key_insights'].append(f"Positive NPV of ${npv['npv']:,.2f} indicates value creation")
                insights['opportunities'].append("Consider expanding similar profitable projects")
            else:
                insights['concerns'].append(f"Negative NPV suggests project may destroy value")
        
        # Analyze working capital
        if 'working_capital' in metrics_results:
            wc = metrics_results['working_capital']
            if wc.get('current_ratio', 0) < 1:
                insights['concerns'].append(f"Low current ratio of {wc['current_ratio']:.2f} indicates liquidity issues")
                insights['risks'].append("May struggle to meet short-term obligations")
                insights['recommendations'].append("Improve cash management and reduce current liabilities")
            elif wc.get('current_ratio', 0) > 2:
                insights['strengths'].append(f"Strong liquidity with current ratio of {wc['current_ratio']:.2f}")
        
        # Analyze debt-to-equity
        if 'debt_to_equity' in metrics_results:
            de = metrics_results['debt_to_equity']
            if de.get('debt_to_equity', 0) > 2:
                insights['risks'].append(f"High leverage with D/E ratio of {de['debt_to_equity']:.2f}")
                insights['recommendations'].append("Consider reducing debt levels or increasing equity")
            elif de.get('debt_to_equity', 0) < 0.5:
                insights['strengths'].append("Conservative capital structure with low debt")
                insights['opportunities'].append("Could leverage debt for growth if profitable")
        
        # General recommendations
        if not insights['concerns']:
            insights['recommendations'].append("Maintain current strong financial performance")
            insights['opportunities'].append("Explore expansion or new market opportunities")
        
        # Add summary insight
        if insights['strengths'] and not insights['concerns']:
            insights['key_insights'].insert(0, "Overall strong financial health with multiple positive indicators")
        elif insights['concerns']:
            insights['key_insights'].insert(0, f"Identified {len(insights['concerns'])} areas requiring attention")
        
        return insights
    
    def suggest_additional_metrics(self, business_type: str, detected_columns: List[str]) -> List[str]:
        """
        Suggest additional metrics based on business type and available data.
        """
        suggestions = []
        
        if business_type == 'retail_inventory':
            suggestions.extend([
                "Stock-to-Sales Ratio",
                "Sell-Through Rate",
                "Average Transaction Value",
                "Customer Lifetime Value",
                "Category Performance Analysis"
            ])
        
        elif business_type == 'service_based':
            suggestions.extend([
                "Billable Hours Percentage",
                "Customer Acquisition Cost",
                "Customer Retention Rate",
                "Average Project Profitability",
                "Resource Utilization Rate"
            ])
        
        elif business_type == 'investment_portfolio':
            suggestions.extend([
                "Sharpe Ratio",
                "Alpha and Beta",
                "Portfolio Volatility",
                "Risk-Adjusted Returns",
                "Diversification Metrics"
            ])
        
        # Common suggestions for all types
        suggestions.extend([
            "Year-over-Year Growth",
            "Burn Rate Analysis",
            "Operating Expense Ratio",
            "EBITDA Margin"
        ])
        
        return suggestions
    
    def detect_anomalies(self, df, financial_data: Dict) -> List[Dict]:
        """
        Detect anomalies and unusual patterns in financial data.
        """
        anomalies = []
        
        # Check for negative values where they shouldn't be
        if 'revenue' in financial_data:
            if any(x < 0 for x in financial_data['revenue']['series']):
                anomalies.append({
                    'type': 'negative_revenue',
                    'severity': 'high',
                    'message': 'Detected negative revenue values - possible data error'
                })
        
        # Check for extreme outliers
        if 'revenue' in financial_data:
            series = financial_data['revenue']['series']
            mean_val = financial_data['revenue']['mean']
            std_val = np.std(series)
            outliers = [x for x in series if abs(x - mean_val) > 3 * std_val]
            if outliers:
                anomalies.append({
                    'type': 'revenue_outliers',
                    'severity': 'medium',
                    'message': f'Detected {len(outliers)} extreme revenue outliers'
                })
        
        # Check for zero or very low profits
        if 'profit' in financial_data:
            if financial_data['profit']['margin'] < 5:
                anomalies.append({
                    'type': 'low_profitability',
                    'severity': 'high',
                    'message': f'Profit margin of {financial_data["profit"]["margin"]:.2f}% is concerning'
                })
        
        return anomalies


def generate_ai_insights(dataset_info: Dict, financial_data: Dict, metrics_results: Dict, api_key: Optional[str] = None) -> Dict:
    """
    Main function to generate AI-powered insights.
    Falls back to rule-based if LLM unavailable.
    """
    analyzer = LLMFinancialAnalyzer(api_key=api_key)
    insights = analyzer.analyze_dataset(dataset_info, financial_data, metrics_results)
    
    # Add anomaly detection
    if 'df' in dataset_info:
        insights['anomalies'] = analyzer.detect_anomalies(dataset_info['df'], financial_data)
    
    # Add metric suggestions
    insights['suggested_metrics'] = analyzer.suggest_additional_metrics(
        dataset_info.get('business_type', 'general'),
        list(dataset_info.get('detected_columns', {}).keys())
    )
    
    return insights


# Mock LLM for testing (when API key not available)
def mock_llm_analysis(prompt: str) -> str:
    """
    Provides mock LLM responses for testing without API key.
    """
    return """
    ## Key Insights
    - Revenue streams are healthy with consistent growth patterns
    - Cost management is effective with good profit margins
    - Strong cash flow position supports business operations
    
    ## Strengths
    - Solid profitability metrics indicate efficient operations
    - Good liquidity ratios suggest financial stability
    
    ## Recommendations
    - Continue monitoring cash flow trends
    - Consider strategic investments in high-ROI areas
    - Optimize inventory levels to improve working capital
    """
