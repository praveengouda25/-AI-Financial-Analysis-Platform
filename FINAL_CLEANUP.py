"""
FINAL PROJECT CLEANUP
Removes all unnecessary documentation and keeps only essential files
"""

import os
from pathlib import Path

# DOCUMENTATION FILES TO DELETE (keep only essential ones)
docs_to_delete = [
    # Workflow and implementation docs (redundant)
    'WORKFLOW_GUIDE.md',
    'RESULTS_EXAMPLES.md',
    'WACC_IMPLEMENTATION_COMPLETE.md',
    'IMPLEMENTATION_COMPLETE.md',
    'FIXES_COMPLETE_SUMMARY.md',
    'FINAL_STATUS_REPORT.md',
    'DATETIME_FIX_AND_API_GUIDE.md',
    'ALL_METRICS_AVAILABLE.md',
    'ADVANCED_PLATFORM_GUIDE.md',
    'QUICKSTART_ADVANCED.md',
    'UPGRADE_COMPARISON.md',
    'HACKATHON_GUIDE.md',
    'PLATFORM_COMPLETE_FINAL.md',
    'SOLUTION_COMPLETE.md',
    'PROJECT_SUMMARY.md',
    
    # Cleanup scripts (already used)
    'CLEANUP_PROJECT.py',
    'cleanup_now.py',
]

# KEEP ONLY THESE ESSENTIAL DOCS:
essential_docs = [
    'README.md',  # Main readme
    'RUPEE_AND_INDUSTRY_UPDATE.md',  # Latest feature guide
    'INDIAN_RUPEE_READY.md',  # Quick start for Indian market
]

print("=" * 70)
print("🧹 FINAL PROJECT CLEANUP")
print("=" * 70)
print("\n📁 Removing redundant documentation files...")
print()

deleted_count = 0
total_size = 0

for filename in docs_to_delete:
    filepath = Path(filename)
    if filepath.exists():
        try:
            size = filepath.stat().st_size
            filepath.unlink()
            print(f"✅ Deleted: {filename} ({size/1024:.1f} KB)")
            deleted_count += 1
            total_size += size
        except Exception as e:
            print(f"❌ Error: {filename} - {e}")
    else:
        print(f"⏭️  Not found: {filename}")

print()
print("=" * 70)
print(f"✅ CLEANUP COMPLETE!")
print(f"   Files deleted: {deleted_count}/{len(docs_to_delete)}")
print(f"   Space freed: {total_size/1024:.1f} KB")
print("=" * 70)

print("\n📚 ESSENTIAL FILES KEPT:")
print("-" * 70)

essential_files = [
    # Core application
    ('app_advanced.py', 'Main Streamlit app (29+ metrics, ₹ support)'),
    
    # Core modules
    ('advanced_calculator.py', 'All financial calculations (NPV, IRR, WACC, EBITDA)'),
    ('smart_analyzer.py', 'Auto dataset analysis'),
    ('llm_integration.py', 'AI insights (OpenAI integration)'),
    ('forecasting_module.py', 'Revenue & profit forecasting'),
    ('industry_kpis.py', 'Industry-specific KPIs'),
    
    # Configuration
    ('requirements_advanced.txt', 'Python dependencies'),
    ('setup_secrets.py', 'OpenAI API key setup'),
    ('.gitignore', 'Git configuration'),
    ('run_app.bat', 'Quick launch script'),
    
    # Testing
    ('test_all_fixes.py', 'Comprehensive test suite'),
    
    # Essential documentation
    ('README.md', 'Project overview'),
    ('RUPEE_AND_INDUSTRY_UPDATE.md', 'Latest features (₹, Forecasting, Industry KPIs)'),
    ('INDIAN_RUPEE_READY.md', 'Quick start guide'),
    
    # Data
    ('sample_input_template.csv', 'Sample dataset template'),
    ('inventory_data.csv', 'Example inventory data'),
]

for filename, description in essential_files:
    if Path(filename).exists():
        size = Path(filename).stat().st_size if Path(filename).is_file() else 0
        print(f"✅ {filename:<35} - {description}")
    else:
        print(f"⚠️  {filename:<35} - NOT FOUND")

print()
print("=" * 70)
print("🎯 PROJECT STATUS:")
print("=" * 70)
print("✅ Core Files: 10 Python modules")
print("✅ Documentation: 3 essential guides")
print("✅ Configuration: 4 files")
print("✅ Tests: 1 comprehensive suite")
print("✅ Data: 2 sample files")
print()
print("📊 Total Essential Files: ~20")
print("🗑️  Removed: Redundant documentation")
print()
print("=" * 70)
print("🚀 READY TO LAUNCH:")
print("=" * 70)
print("   python -m streamlit run app_advanced.py")
print("=" * 70)
