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

themes = ['vnstock', 'academic', 'minimal']
langs = ['vi', 'en']

for theme in themes:
    print(f"\n{'='*50}")
    print(f"GENERATING CHARTS FOR THEME: {theme.upper()}")
    print(f"{'='*50}")
    for lang in langs:
        print(f"\n--- Language: {lang.upper()} ---")
        for script in scripts:
            print(f"Running {script}...")
            subprocess.run(['python3', os.path.join('examples', script), '--lang', lang, '--theme', theme], check=True)

print("\nĐã hoàn tất sinh toàn bộ bộ sưu tập biểu đồ song ngữ đa theme!")
