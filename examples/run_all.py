import os
import subprocess

scripts = [
    '01_performance_risk.py',
    '02_technical_analysis.py',
    '03_portfolio_management.py',
    '04_market_data.py',
    '05_enterprise_analysis.py',
    '06_summary_cards.py',
    '07_backtest.py'
]

# Generate Vietnamese version (default)
print("--- GENERATING VIETNAMESE CHARTS ---")
for script in scripts:
    print(f"Running {script} (vi)...")
    subprocess.run(['python3', os.path.join('examples', script), '--lang', 'vi'], check=True)

# Generate English version
print("\n--- GENERATING ENGLISH CHARTS ---")
for script in scripts:
    print(f"Running {script} (en)...")
    subprocess.run(['python3', os.path.join('examples', script), '--lang', 'en'], check=True)

print("\nĐã hoàn tất sinh toàn bộ bộ sưu tập biểu đồ song ngữ!")
