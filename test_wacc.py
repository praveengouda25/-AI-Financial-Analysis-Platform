"""
Quick test to verify WACC calculation is working
"""

from advanced_calculator import AdvancedFinancialCalculator

# Test WACC calculation
print("=" * 70)
print("🧪 TESTING WACC CALCULATION")
print("=" * 70)

calc = AdvancedFinancialCalculator()

# Test 1: Basic WACC calculation
print("\nTest 1: Basic WACC Calculation")
print("-" * 70)
wacc = calc.calculate_wacc(
    equity=500000,
    debt=300000,
    cost_of_equity=0.12,
    cost_of_debt=0.06,
    tax_rate=0.30
)

if 'error' in wacc:
    print(f"❌ ERROR: {wacc['error']}")
else:
    print(f"✅ WACC: {wacc['wacc_percentage']:.2f}%")
    print(f"✅ Equity Weight: {wacc['equity_weight']*100:.1f}%")
    print(f"✅ Debt Weight: {wacc['debt_weight']*100:.1f}%")
    print(f"✅ Total Capital: ₹{wacc['total_capital']:,.0f}")
    print(f"✅ After-tax Cost of Debt: {wacc['after_tax_cost_of_debt']*100:.2f}%")

# Test 2: Test with financial_data format (as used in app)
print("\n\nTest 2: WACC from Financial Data")
print("-" * 70)

financial_data = {
    'equity': 600000,
    'liabilities': 400000,
    'revenue': {'total': 1000000, 'mean': 100000, 'series': [100000]},
    'cost': {'total': 600000, 'mean': 60000, 'series': [60000]}
}

results = calc.calculate_all_metrics(financial_data)

if 'wacc' in results:
    wacc_result = results['wacc']
    if 'error' in wacc_result:
        print(f"❌ ERROR: {wacc_result['error']}")
    else:
        print(f"✅ WACC Calculated Successfully!")
        print(f"   WACC: {wacc_result['wacc_percentage']:.2f}%")
        print(f"   Equity: ₹{wacc_result['equity']:,.0f}")
        print(f"   Debt: ₹{wacc_result['debt']:,.0f}")
        print(f"   Interpretation: {wacc_result['interpretation']}")
else:
    print("❌ WACC not calculated - missing from results")

# Test 3: Test with sample CSV data structure
print("\n\nTest 3: Sample Dataset Test")
print("-" * 70)
print("Create a CSV file with these columns:")
print("   Equity, Liabilities, Revenue, Cost")
print("   500000, 300000, 1000000, 600000")
print("\nWhen uploaded, WACC should calculate to ~9.15%")

print("\n" + "=" * 70)
print("✅ WACC TESTING COMPLETE")
print("=" * 70)
print("\n💡 To test in app:")
print("   1. Create CSV with Equity and Liabilities columns")
print("   2. Upload to app_advanced.py")
print("   3. Check Tab 8: 'Advanced (WACC, EBITDA)'")
print("=" * 70)
