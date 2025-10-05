"""
Advanced Automated Financial Analysis Platform
Full automation with LLM integration for any business dataset
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from pathlib import Path
import sys

# Import custom modules
from smart_analyzer import SmartFinancialAnalyzer, auto_detect_and_calculate
from advanced_calculator import AdvancedFinancialCalculator
from llm_integration import generate_ai_insights

# Page configuration
st.set_page_config(
    page_title="ZENALYST.AI Financial Analysis ",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e3f2fd;
        border-left: 5px solid #1976d2;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #0d47a1;
        font-weight: 500;
    }
    .warning-box {
        background-color: #fff9e6;
        border-left: 5px solid #ff9800;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #e65100;
        font-weight: 500;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #1b5e20;
        font-weight: 500;
    }
    .risk-box {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #b71c1c;
        font-weight: 500;
    }
    .recommendation-box {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #4a148c;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


def display_header():
    """Display application header."""
    st.markdown('<div class="main-header">🤖AI Financial Analysis Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated Financial Intelligence for Any Business • LLM-Enhanced Insights</div>', unsafe_allow_html=True)
    st.markdown("---")


def load_and_process_file(uploaded_file=None, file_path=None):
    """
    Load and process any CSV/Excel file with smart detection.
    Handles datetime columns and ensures only numeric data is used for calculations.
    """
    try:
        if uploaded_file is not None:
            # Read file based on extension
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                try:
                    df = pd.read_csv(uploaded_file)
                except Exception as e:
                    return None, None, f"Failed to read CSV file: {str(e)}. File may be corrupted."
            elif file_extension in ['xlsx', 'xls']:
                try:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                except Exception as e:
                    return None, None, f"Failed to read Excel file: {str(e)}. File may be corrupted or password-protected."
            else:
                return None, None, f"Unsupported file format: .{file_extension}. Please upload CSV or Excel files."
        
        elif file_path is not None:
            if not Path(file_path).exists():
                return None, None, f"File not found: {file_path}"
            
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path, engine='openpyxl')
            except Exception as e:
                return None, None, f"Failed to read file: {str(e)}"
        
        else:
            return None, None, "No file provided"
        
        # Validate dataframe
        if df is None or df.empty:
            return None, None, "File is empty or contains no data"
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Check if we have at least some numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return None, None, "No numeric columns found in dataset. Please ensure your file contains financial data with numbers."
        
        # Automatic analysis (handles datetime columns internally)
        try:
            analysis_result = auto_detect_and_calculate(df)
        except Exception as e:
            return None, None, f"Error analyzing dataset: {str(e)}"
        
        return df, analysis_result, None
    
    except Exception as e:
        return None, None, f"Error processing file: {str(e)}"


def display_business_detection(analysis):
    """Display business type detection results."""
    st.subheader("🔍 Automatic Business Intelligence")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Business Type</h3>
            <p style="font-size: 1.5rem; margin: 0;">{analysis['business_type'].replace('_', ' ').title()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        detected = len(analysis['detected_columns'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>Columns Detected</h3>
            <p style="font-size: 1.5rem; margin: 0;">{detected} Financial Fields</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        metrics_count = len(analysis['available_metrics'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>Metrics Available</h3>
            <p style="font-size: 1.5rem; margin: 0;">{metrics_count} Calculations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show detected columns
    with st.expander("📊 Detected Financial Columns"):
        cols = st.columns(3)
        for idx, (key, value) in enumerate(analysis['detected_columns'].items()):
            with cols[idx % 3]:
                st.markdown(f"**{key.title()}:** `{value}`")
    
    # Show recommendations
    if analysis['recommendations']:
        st.markdown("### 💡 Smart Recommendations")
        for rec in analysis['recommendations']:
            st.markdown(f"- {rec}")


def display_financial_metrics(metrics_results):
    """Display all calculated financial metrics."""
    st.subheader("📈 Automated Financial Metrics")
    
    tabs = st.tabs([
        "Profit/Loss", "Returns", "Cash Flow", "Margins", 
        "Liquidity", "Leverage", "Efficiency", "Advanced (WACC, EBITDA)"
    ])
    
    # Tab 1: Profit/Loss
    with tabs[0]:
        if 'profit_loss' in metrics_results:
            pl = metrics_results['profit_loss']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Net Profit/Loss", f"₹{pl['profit']:,.2f}", 
                         delta=f"{pl['profit_percentage']:.2f}%")
            with col2:
                st.metric("Total Revenue", f"₹{pl['revenue']:,.2f}")
            with col3:
                st.metric("Total Costs", f"₹{pl['cost']:,.2f}")
            with col4:
                status = "🟢 Profitable" if pl['is_profitable'] else "🔴 Loss"
                st.metric("Status", status)
            
            # Profit/Loss Chart
            fig = go.Figure(data=[
                go.Bar(name='Revenue', x=['Financial Performance'], y=[pl['revenue']], marker_color='green'),
                go.Bar(name='Costs', x=['Financial Performance'], y=[pl['cost']], marker_color='red'),
                go.Bar(name='Profit', x=['Financial Performance'], y=[pl['profit']], marker_color='blue')
            ])
            fig.update_layout(
                title='Revenue vs Costs vs Profit',
                barmode='group',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"**Interpretation:** {pl['interpretation']}")
    
    # Tab 2: Returns (ROI, NPV, IRR)
    with tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'roi' in metrics_results:
                roi = metrics_results['roi']
                st.markdown("#### 💰 Return on Investment (ROI)")
                st.metric("ROI", f"{roi['roi_percentage']:.2f}%", 
                         delta="Positive" if roi['roi'] > 0 else "Negative")
                st.info(roi['interpretation'])
        
        with col2:
            if 'npv' in metrics_results:
                npv = metrics_results['npv']
                st.markdown("#### 📊 Net Present Value (NPV)")
                st.metric("NPV", f"₹{npv['npv']:,.2f}",
                         delta=npv['decision'])
                st.info(npv['interpretation'])
        
        if 'irr' in metrics_results:
            irr = metrics_results['irr']
            st.markdown("#### 📈 Internal Rate of Return (IRR)")
            st.metric("IRR", f"{irr['irr_percentage']:.2f}%",
                     delta=irr['recommendation'])
            st.info(irr['interpretation'])
    
    # Tab 3: Cash Flow
    with tabs[2]:
        if 'cashflow_analysis' in metrics_results:
            cf = metrics_results['cashflow_analysis']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Net Cash Flow", f"₹{cf['net_cashflow']:,.2f}")
            with col2:
                st.metric("Cash Flow Margin", f"{cf['cashflow_margin_percentage']:.2f}%")
            with col3:
                st.metric("Status", cf['status'], delta="Good" if cf['status'] == 'Positive' else "Concern")
            
            st.info(f"**Analysis:** {cf['interpretation']}")
        
        # NPV Cash Flow Chart
        if 'npv' in metrics_results and 'present_values' in metrics_results['npv']:
            npv = metrics_results['npv']
            periods = list(range(len(npv['present_values'])))
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=periods,
                y=npv['present_values'],
                name='Present Values',
                marker_color='lightblue'
            ))
            fig.update_layout(
                title='NPV Cash Flow Analysis by Period',
                xaxis_title='Period',
                yaxis_title='Present Value (₹)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Margins
    with tabs[3]:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'gross_margin' in metrics_results:
                gm = metrics_results['gross_margin']
                st.markdown("#### Gross Profit Margin")
                st.metric("Margin", f"{gm['gross_margin_percentage']:.2f}%")
                st.metric("Gross Profit", f"₹{gm['gross_profit']:,.2f}")
                st.info(gm['interpretation'])
        
        with col2:
            if 'net_margin' in metrics_results:
                nm = metrics_results['net_margin']
                st.markdown("#### Net Profit Margin")
                st.metric("Margin", f"{nm['net_margin_percentage']:.2f}%")
                st.metric("Net Profit", f"₹{nm['net_profit']:,.2f}")
                st.info(nm['interpretation'])
    
    # Tab 5: Liquidity
    with tabs[4]:
        if 'working_capital' in metrics_results:
            wc = metrics_results['working_capital']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Working Capital", f"₹{wc['working_capital']:,.2f}")
            with col2:
                st.metric("Current Ratio", f"{wc['current_ratio']:.2f}")
            with col3:
                st.metric("Liquidity Status", wc['liquidity_status'])
            
            st.info(f"**Analysis:** {wc['interpretation']}")
            
            # Liquidity Chart
            fig = go.Figure(data=[
                go.Bar(name='Current Assets', x=['Liquidity'], y=[wc['current_assets']], marker_color='green'),
                go.Bar(name='Current Liabilities', x=['Liquidity'], y=[wc['current_liabilities']], marker_color='orange')
            ])
            fig.update_layout(title='Current Assets vs Liabilities', height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 6: Leverage
    with tabs[5]:
        if 'debt_to_equity' in metrics_results:
            de = metrics_results['debt_to_equity']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("D/E Ratio", f"{de['debt_to_equity']:.2f}")
            with col2:
                st.metric("Total Debt", f"₹{de['total_debt']:,.2f}")
            with col3:
                st.metric("Leverage", de['leverage'])
            
            st.info(f"**Analysis:** {de['interpretation']}")
            
            # Leverage Pie Chart
            fig = go.Figure(data=[go.Pie(
                labels=['Debt', 'Equity'],
                values=[de['total_debt'], de['total_equity']],
                hole=.3
            )])
            fig.update_layout(title='Capital Structure', height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 7: Efficiency
    with tabs[6]:
        if 'inventory_turnover' in metrics_results:
            it = metrics_results['inventory_turnover']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Inventory Turnover", f"{it['inventory_turnover']:.2f}x")
            with col2:
                st.metric("Days Inventory", f"{it['days_inventory_outstanding']:.0f} days")
            with col3:
                st.metric("Efficiency", it['efficiency'])
            
            st.info(f"**Analysis:** {it['interpretation']}")
    
    # Tab 8: Advanced Metrics (WACC, EBITDA, etc.)
    with tabs[7]:
        st.markdown("### 💼 Advanced Financial Metrics")
        
        # WACC
        if 'wacc' in metrics_results:
            wacc = metrics_results['wacc']
            
            if 'error' not in wacc:
                st.markdown("#### WACC (Weighted Average Cost of Capital)")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("WACC", f"{wacc['wacc_percentage']:.2f}%")
                with col2:
                    st.metric("Equity Weight", f"{wacc['equity_weight']*100:.1f}%")
                with col3:
                    st.metric("Debt Weight", f"{wacc['debt_weight']*100:.1f}%")
                
                # Detailed breakdown
                with st.expander("📊 WACC Breakdown"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Total Capital:** ₹{wacc['total_capital']:,.2f}")
                        st.write(f"**Equity:** ₹{wacc['equity']:,.2f}")
                        st.write(f"**Debt:** ₹{wacc['debt']:,.2f}")
                    with col2:
                        st.write(f"**Cost of Equity:** {wacc['cost_of_equity']*100:.1f}%")
                        st.write(f"**Cost of Debt:** {wacc['cost_of_debt']*100:.1f}%")
                        st.write(f"**Tax Rate:** {wacc['tax_rate']*100:.1f}%")
                
                st.info(f"**Interpretation:** {wacc['interpretation']}")
                st.success(f"💡 **{wacc['recommendation']}**")
                
                # WACC Visualization
                fig = go.Figure(data=[go.Pie(
                    labels=['Equity Component', 'Debt Component (After-Tax)'],
                    values=[
                        wacc['equity_weight'] * wacc['cost_of_equity'],
                        wacc['debt_weight'] * wacc['after_tax_cost_of_debt']
                    ],
                    hole=.4
                )])
                fig.update_layout(title='WACC Components', height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # EBITDA
        if 'ebitda' in metrics_results:
            ebitda = metrics_results['ebitda']
            
            if 'error' not in ebitda:
                st.markdown("#### EBITDA Analysis")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("EBITDA", f"₹{ebitda['ebitda']:,.2f}")
                with col2:
                    st.metric("EBITDA Margin", f"{ebitda['ebitda_margin']:.2f}%")
                with col3:
                    st.metric("Status", ebitda['status'])
                with col4:
                    st.metric("Revenue", f"₹{ebitda['revenue']:,.2f}")
                
                st.info(f"**Analysis:** {ebitda['interpretation']}")
                
                # EBITDA Chart
                fig = go.Figure(data=[
                    go.Bar(name='EBITDA', x=['Performance'], y=[ebitda['ebitda']], marker_color='lightblue'),
                    go.Bar(name='Operating Expenses', x=['Performance'], y=[ebitda['operating_expenses']], marker_color='coral')
                ])
                fig.update_layout(title='EBITDA vs Operating Expenses', barmode='group', height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        # Show if no advanced metrics available
        if 'wacc' not in metrics_results and 'ebitda' not in metrics_results:
            st.warning("⚠️ **Advanced metrics not available**\n\nThese metrics require:\n- **WACC:** Equity and Debt/Liabilities data\n- **EBITDA:** Revenue and Operating Expenses data")
            st.info("💡 Upload a dataset with balance sheet information to see WACC, or income statement data for EBITDA.")


def display_ai_insights(insights):
    """Display LLM-generated insights."""
    st.subheader("🤖 AI-Powered Insights & Recommendations")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Key Insights", "Recommendations", "Risks & Opportunities", "Anomalies"
    ])
    
    with tab1:
        if insights.get('key_insights'):
            for insight in insights['key_insights']:
                st.markdown(f"""
                <div class="insight-box">
                    <strong>🔍</strong> {insight}
                </div>
                """, unsafe_allow_html=True)
        
        if insights.get('strengths'):
            st.markdown("### ✅ Strengths")
            for strength in insights['strengths']:
                st.success(f"✓ {strength}")
        
        if insights.get('concerns'):
            st.markdown("### ⚠️ Concerns")
            for concern in insights['concerns']:
                st.warning(f"⚠ {concern}")
    
    with tab2:
        if insights.get('recommendations'):
            st.markdown("### 💡 Actionable Recommendations")
            for idx, rec in enumerate(insights['recommendations'], 1):
                st.markdown(f"""
                <div class="success-box">
                    <strong>{idx}.</strong> {rec}
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            if insights.get('risks'):
                st.markdown("### ⚠️ Risk Assessment")
                for risk in insights['risks']:
                    st.markdown(f"""
                    <div class="warning-box">
                        <strong>🔸</strong> {risk}
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            if insights.get('opportunities'):
                st.markdown("### 🎯 Growth Opportunities")
                for opp in insights['opportunities']:
                    st.markdown(f"""
                    <div class="success-box">
                        <strong>📈</strong> {opp}
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab4:
        if insights.get('anomalies'):
            st.markdown("### 🔍 Detected Anomalies")
            for anomaly in insights['anomalies']:
                severity_color = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }
                color = severity_color.get(anomaly.get('severity', 'low'), '🔵')
                st.warning(f"{color} **{anomaly.get('type', 'Anomaly').replace('_', ' ').title()}:** {anomaly.get('message', 'Detected')}")


def display_comprehensive_dashboard(df, financial_data):
    """Display comprehensive visual dashboard."""
    st.subheader("📊 Interactive Dashboard")
    
    # Revenue and Cost Trends
    if 'revenue' in financial_data and 'dates' in financial_data:
        fig = go.Figure()
        
        if financial_data['dates'] is not None:
            fig.add_trace(go.Scatter(
                x=financial_data['dates'],
                y=financial_data['revenue']['series'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='green', width=2)
            ))
            
            if 'cost' in financial_data:
                fig.add_trace(go.Scatter(
                    x=financial_data['dates'],
                    y=financial_data['cost']['series'],
                    mode='lines+markers',
                    name='Costs',
                    line=dict(color='red', width=2)
                ))
            
            fig.update_layout(
                title='Revenue & Cost Trends Over Time',
                xaxis_title='Date',
                yaxis_title='Amount (₹)',
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Summary Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Key Statistics")
        stats_df = df.describe().T
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Data Distribution")
        # Show distribution of numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select column to visualize", numeric_cols)
            fig = px.histogram(df, x=selected_col, nbins=30, title=f'Distribution of {selected_col}')
            st.plotly_chart(fig, use_container_width=True)


def main():
    """Main application function."""
    display_header()
    
    # Sidebar configuration
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
        st.title("Configuration")
        
        # LLM API Key (optional)
        st.markdown("### 🤖 AI Insights")
        use_llm = st.checkbox("Enable AI Insights (OpenAI)", value=False)
        api_key = None
        
        if use_llm:
            st.info("💡 **OpenAI API Key Setup:**\n\n"
                   "**Option 1:** Enter below\n"
                   "**Option 2:** Set in `.streamlit/secrets.toml`\n"
                   "**Option 3:** Set environment variable `OPENAI_API_KEY`")
            
            # Try to get API key from multiple sources
            api_key_input = st.text_input("OpenAI API Key", type="password", 
                                         help="Enter your OpenAI API key or leave blank to use secrets/env variable")
            
            # Priority: User input > Streamlit secrets > Environment variable
            if api_key_input:
                api_key = api_key_input
            elif hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                api_key = st.secrets['OPENAI_API_KEY']
                st.success("✅ Using API key from secrets")
            else:
                import os
                api_key = os.getenv('OPENAI_API_KEY')
                if api_key:
                    st.success("✅ Using API key from environment")
                else:
                    st.warning("⚠️ No API key found. Enter above or configure in secrets/environment.")
            
            with st.expander("📖 How to get OpenAI API Key"):
                st.markdown("""
                1. Go to [platform.openai.com](https://platform.openai.com)
                2. Sign up or log in
                3. Navigate to API Keys section
                4. Create new secret key
                5. Copy and paste here
                
                **Security Best Practice:**
                - Store in `.streamlit/secrets.toml`:
                  ```toml
                  OPENAI_API_KEY = "sk-..."
                  ```
                - Or set environment variable:
                  ```bash
                  export OPENAI_API_KEY="sk-..."
                  ```
                """)
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        **AI-Powered Financial Analysis Platform**
        
        ✅ Automatic dataset detection
        ✅ 15+ financial metrics
        ✅ LLM-enhanced insights
        ✅ Interactive visualizations
        ✅ Production-ready
        """)
    
    # Main content area
    st.markdown("## 📁 Upload Your Financial Dataset")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload any financial/business dataset - the system will automatically detect and analyze it"
        )
    
    with col2:
        st.markdown("### Quick Start")
        use_sample = st.button("📦 Load Sample Dataset", use_container_width=True)
    
    # Process file
    df = None
    analysis_result = None
    error_msg = None
    
    if uploaded_file is not None:
        with st.spinner("🔄 Analyzing your dataset with AI..."):
            df, analysis_result, error_msg = load_and_process_file(uploaded_file=uploaded_file)
    
    elif use_sample:
        sample_path = Path('data/Hackathon/Inputs/ABC_Book_Stores_Inventory_Register.xlsx')
        if sample_path.exists():
            with st.spinner("🔄 Loading sample dataset..."):
                df, analysis_result, error_msg = load_and_process_file(file_path=str(sample_path))
        else:
            st.error("❌ Sample dataset not found. Please upload your own file.")
            return
    
    else:
        st.info("👆 **Get Started:** Upload your financial dataset or load the sample to see automatic analysis in action!")
        
        # Show feature showcase
        st.markdown("---")
        st.markdown("## 🚀 Platform Capabilities")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 📊 Automatic Detection
            - Business type identification
            - Column mapping
            - Data quality assessment
            - Metric recommendations
            """)
        
        with col2:
            st.markdown("""
            ### 💰 Financial Metrics
            - Profit/Loss Analysis
            - ROI, NPV, IRR
            - Cash Flow Analysis
            - Margins & Ratios
            """)
        
        with col3:
            st.markdown("""
            ### 🤖 AI Insights
            - LLM-powered analysis
            - Anomaly detection
            - Risk assessment
            - Growth opportunities
            """)
        
        return
    
    # Handle errors
    if error_msg:
        st.error(f"❌ {error_msg}")
        st.markdown("""
        **Troubleshooting:**
        - Ensure file is not corrupted
        - Check file format (CSV or Excel)
        - Verify data contains financial information
        """)
        return
    
    if df is None or analysis_result is None:
        st.error("❌ Failed to process dataset. Please try again.")
        return
    
    # Success! Display results
    st.success(f"✅ Dataset analyzed successfully! Found **{len(df)} records** with **{len(df.columns)} columns**")
    
    # Display business intelligence
    display_business_detection(analysis_result['analysis'])
    
    st.markdown("---")
    
    # Calculate all metrics
    financial_data = analysis_result['financial_data']
    calculator = AdvancedFinancialCalculator()
    metrics_results = calculator.calculate_all_metrics(financial_data)
    
    # Display financial metrics
    display_financial_metrics(metrics_results)
    
    st.markdown("---")
    
    # Generate and display AI insights
    if use_llm and api_key:
        with st.spinner("🤖 Generating AI insights..."):
            try:
                ai_insights = generate_ai_insights(
                    {'business_type': analysis_result['analysis']['business_type'], 
                     'data_quality': analysis_result['analysis']['data_quality'],
                     'df': df},
                    financial_data,
                    metrics_results,
                    api_key=api_key
                )
                display_ai_insights(ai_insights)
            except Exception as e:
                st.warning(f"⚠️ AI insights unavailable: {str(e)}")
                st.info("Showing rule-based insights instead...")
                ai_insights = generate_ai_insights(
                    {'business_type': analysis_result['analysis']['business_type'],
                     'data_quality': analysis_result['analysis']['data_quality']},
                    financial_data,
                    metrics_results
                )
                display_ai_insights(ai_insights)
    else:
        with st.spinner("🤖 Generating insights..."):
            ai_insights = generate_ai_insights(
                {'business_type': analysis_result['analysis']['business_type'],
                 'data_quality': analysis_result['analysis']['data_quality']},
                financial_data,
                metrics_results
            )
            display_ai_insights(ai_insights)
    
    st.markdown("---")
    
    # Display comprehensive dashboard
    display_comprehensive_dashboard(df, financial_data)
    
    st.markdown("---")
    
    # Export functionality
    st.subheader("💾 Export Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Full Report to Excel", use_container_width=True):
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"financial_analysis_{timestamp}.xlsx"
                
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    # Raw data
                    df.to_excel(writer, sheet_name='Raw_Data', index=False)
                    
                    # Metrics summary
                    metrics_df = pd.DataFrame([
                        {k: str(v) for k, v in metric.items()} 
                        for metric in metrics_results.values()
                    ])
                    metrics_df.to_excel(writer, sheet_name='Metrics', index=False)
                    
                    # Insights
                    if 'key_insights' in ai_insights:
                        insights_df = pd.DataFrame({
                            'Insights': ai_insights.get('key_insights', []),
                            'Recommendations': ai_insights.get('recommendations', [])[:len(ai_insights.get('key_insights', []))]
                        })
                        insights_df.to_excel(writer, sheet_name='AI_Insights', index=False)
                
                st.success(f"✅ Report exported: {filename}")
                
                with open(filename, 'rb') as f:
                    st.download_button(
                        label="📥 Download Report",
                        data=f,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"❌ Export failed: {str(e)}")
    
    with col2:
        with st.expander("📄 View Raw Data"):
            st.dataframe(df, use_container_width=True, height=400)


if __name__ == "__main__":
    main()
