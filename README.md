<div align="right">
  
[1]: https://github.com/praveengouda25
[2]: https://www.linkedin.com/in/praveen-kumar-bcc2525/

[![github](https://github.com/praveengouda25/Telecom_Customer_Churn_Prediction/blob/4f3921b8f8104e2a1fd9ff8dbf2191765a89e228/icons/git.svg)][1]
[![linkedin](https://github.com/praveengouda25/Telecom_Customer_Churn_Prediction/blob/7cdd63bd3820d6a3cc1d61d0a78f976d942c9ea6/icons/linkedin.svg)][2]

</div>


# <div align="center"># 💰 AUTOMATED FINANCIAL ANALYSIS </div>

![AI FINANCIAL ANALYSIS PLATFORM](https://github.com/praveengouda25/-AI-Financial-Analysis-Platform/blob/5738f03d8be8db27bd57f1fe7befa48a3bcccd5e/images/FIRST.png)  



A professional Python-based financial analysis tool that automates the calculation of sophisticated financial metrics with an interactive Streamlit dashboard.
AI FINANCIAL ANALYSIS PLATFORM WEB-APP: 

## 📊 Features

### Supported Financial Metrics
1. **WACC (Weighted Average Cost of Capital)** - Calculates the firm's overall cost of capital
2. **ROI (Return on Investment)** - Measures investment profitability
3. **Debt-to-Equity Ratio** - Analyzes financial leverage
4. **NPV (Net Present Value)** - Evaluates project profitability
5. **IRR (Internal Rate of Return)** - Determines investment yield

# BUSINESS INTELLIGENCE ANALYSIS
![BUSINESS INTELLIGENCE ANALYSIS](https://github.com/praveengouda25/-AI-Financial-Analysis-Platform/blob/0cb1ad5d215d06f3650fcffd2f738de81719ae3d/images/BI%20DASHBOARD.png)  


### Key Capabilities
- ✅ **Dual Input Methods**: Manual entry or batch upload (Excel/CSV)
- ✅ **Live Calculations**: Real-time metric computation
- ✅ **Formula Transparency**: View formulas and step-by-step calculations
- ✅ **Export Functionality**: Save results to formatted Excel files
- ✅ **Input Validation**: Robust error handling for invalid data
- ✅ **4 Decimal Precision**: Accurate financial calculations
- ✅ **Professional UI**: Hackathon-ready Streamlit dashboard

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Usage Guide

### Method 1: Manual Input

1. Select **"Manual Input"** option
2. Navigate through metric tabs (WACC, ROI, D/E Ratio, NPV, IRR)
3. Enter required financial data
4. Click **"Calculate"** button
5. View results with formulas and interpretations
6. Export all calculations to Excel

### Method 2: File Upload

1. Select **"File Upload"** option
2. Prepare Excel/CSV file with column headers matching parameter names:
   - For WACC: `equity`, `debt`, `cost_of_equity`, `cost_of_debt`, `tax_rate`
   - For ROI: `initial_investment`, `final_value`
   - For D/E: `total_debt`, `total_equity`
   - For NPV: `discount_rate`, `cash_flows`, `npv_initial_investment` (optional)
   - For IRR: `irr_cash_flows`
3. Upload file
4. Click **"Calculate Metrics from File"**
5. Download results as Excel file

# Revenue vs Cost vs Profit
![Revenue vs cost vs profit](https://github.com/praveengouda25/-AI-Financial-Analysis-Platform/blob/1bcf314b8ec43d3df83c81c3d72eb831a28122a4/images/profit_plot.png) 

## 📋 Example Input File Format

### Excel/CSV Template

| equity | debt | cost_of_equity | cost_of_debt | tax_rate | initial_investment | final_value |
|--------|------|----------------|--------------|----------|-------------------|-------------|
| 1000000| 500000| 0.12          | 0.08         | 0.30     | 100000            | 150000      |

**Note**: 
- Rates should be in decimal format (e.g., 0.12 for 12%)
- Cash flows for NPV/IRR should be comma-separated strings (e.g., "-100000, 30000, 40000")

## 🧮 Calculation Details

### WACC Formula
```
WACC = (E/V) × Re + (D/V) × Rd × (1 - Tc)
```
- E = Market value of equity
- D = Market value of debt
- V = Total value (E + D)
- Re = Cost of equity
- Rd = Cost of debt
- Tc = Corporate tax rate

![](https://github.com/praveengouda25/-AI-Financial-Analysis-Platform/blob/ee51f667e3becd0bcc1f9d64d45cf1a77836f86f/images/EBITA%20ANLYSIS.png) 

### ROI Formula
```
ROI = (Final Value - Initial Investment) / Initial Investment
```

### Debt-to-Equity Ratio
```
D/E Ratio = Total Debt / Total Equity
```

### NPV Formula
```
NPV = Σ [CFt / (1 + r)^t] - Initial Investment
```
- CFt = Cash flow at time t
- r = Discount rate
- t = Time period

# NET PRESENT VALUE(NPV):
![NET PRESENT VALUE(NPV)](https://github.com/praveengouda25/-AI-Financial-Analysis-Platform/blob/fb1163940fa38dcebdf12ade83b3c399a628f598/images/NPV.png) 



### IRR Calculation
IRR is the rate where NPV = 0:
```
0 = Σ [CFt / (1 + IRR)^t]
```

## 📁 Project Structure

```
automation-metrics-calculator/
│
├── calculator.py          # Core financial calculation functions
├── app.py                 # Streamlit UI application
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
└── outputs/              # Generated Excel reports (auto-created)
```

## 🔧 Technical Stack

- **Python 3.8+**
- **Streamlit** - Interactive web UI
- **pandas** - Data manipulation and Excel I/O
- **numpy** - Financial calculations and IRR
- **openpyxl** - Excel file handling

## ✨ Key Functions (calculator.py)

### Core Calculation Functions
- `calculate_wacc()` - Weighted Average Cost of Capital
- `calculate_roi()` - Return on Investment
- `calculate_debt_to_equity()` - Debt-to-Equity Ratio
- `calculate_npv()` - Net Present Value
- `calculate_irr()` - Internal Rate of Return

### Utility Functions
- `calculate_all_metrics()` - Batch calculation from dictionary
- `read_excel_input()` - Import from Excel
- `read_csv_input()` - Import from CSV
- `export_results_to_excel()` - Export results with formatting

### Validation Functions
- `validate_positive()` - Ensure positive values
- `validate_non_negative()` - Ensure non-negative values
- `validate_rate()` - Validate percentage rates (0-100%)

## 🎯 Validation & Error Handling

The calculator includes comprehensive validation:
- ✅ Positive value checks for investments and capital
- ✅ Rate bounds validation (0-100%)
- ✅ Division by zero prevention
- ✅ Empty data detection
- ✅ Cash flow consistency checks
- ✅ File format validation

All errors are caught and displayed with clear, actionable messages.

## 📊 Output Format

### Excel Export Structure
Generated Excel files contain multiple sheets:
- **Summary** - All metrics at a glance
- **WACC** - Detailed WACC calculation
- **ROI** - ROI breakdown
- **Debt_to_Equity** - D/E ratio analysis
- **NPV** - NPV with cash flow breakdown
- **IRR** - IRR calculation details

Each sheet includes:
- Calculated values (4 decimal precision)
- Formulas used
- Step-by-step calculations
- Interpretations and decisions

![](https://github.com/praveengouda25/-AI-Financial-Analysis-Platform/blob/aca5573bc34eb2a82bea384824a4d59596ab9d55/images/REVENUE%20COST%20PLOT.png)



## 🏆Features

- **Professional UI** - Modern, clean design
- **Responsive Layout** - Works on all screen sizes
- **Real-time Calculations** - Instant feedback
- **Formula Transparency** - Educational and verifiable
- **Export Functionality** - Share results easily
- **Error Handling** - User-friendly error messages
- **Code Quality** - Clean, modular, commented code

## 🔐 Best Practices Implemented

1. **Modular Design** - Separated calculation logic from UI
2. **Type Hints** - Clear function signatures
3. **Docstrings** - Comprehensive function documentation
4. **Input Validation** - Robust error handling
5. **Decimal Precision** - Consistent 4-decimal accuracy
6. **Professional Styling** - Custom CSS for polished look
7. **User Experience** - Intuitive interface with helpful tooltips

## 🧪 Testing

### Manual Testing
1. Test each metric with known values
2. Verify against Excel calculations
3. Test edge cases (zero values, negative cash flows)
4. Validate error messages

### Sample Test Cases

**WACC Test**:
- Equity: $1,000,000
- Debt: $500,000
- Cost of Equity: 12%
- Cost of Debt: 8%
- Tax Rate: 30%
- Expected WACC: ≈ 9.73%

**ROI Test**:
- Initial Investment: $100,000
- Final Value: $150,000
- Expected ROI: 50%

**NPV Test**:
- Discount Rate: 10%
- Cash Flows: [-100000, 30000, 40000, 50000, 40000]
- Expected NPV: ≈ $19,019.45

## 📝 Future Enhancements

Potential additions for extended versions:
- Additional metrics (CAGR, Sharpe Ratio, Beta, etc.)
- Historical data analysis
- Scenario analysis and sensitivity testing
- Interactive charts and visualizations
- Database integration for data persistence
- API endpoints for programmatic access
- Multi-currency support

## 🤝 Contributing

This is a hackathon project. Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Optimize calculations

## 📄 License

This project is created for educational and hackathon purposes.

## 👨‍💻 Developer Notes

### Code Organization
- **calculator.py**: Pure calculation logic, no UI dependencies
- **app.py**: Streamlit UI, imports from calculator.py
- Clean separation allows for easy testing and maintenance

### Adding New Metrics
1. Add calculation function to `calculator.py`
2. Add validation logic
3. Create UI tab in `app.py`
4. Update `calculate_all_metrics()` for batch processing
5. Add export logic in `export_results_to_excel()`

## 📞 Support

For issues or questions:
1. Check error messages (they're descriptive!)
2. Review this README
3. Verify input data format
4. Ensure all dependencies are installed

---

**Built with ❤️ for# 🤖 ZENALYST.AI - AI-Powered Financial Analysis Platform

## Comprehensive Financial Intelligence for Indian Businesses

A production-ready Streamlit application that automatically analyzes financial datasets and calculates 40+ metrics including NPV, IRR, WACC, EBITDA, forecasting, and industry-specific KPIs - all in Indian Rupees (₹).ng Financial Analysis Simple and Accurate*
