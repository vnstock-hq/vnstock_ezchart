import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vnstock_ezchart import Chart

parser = argparse.ArgumentParser()
parser.add_argument('--lang', type=str, default='vi', choices=['vi', 'en'])
args, _ = parser.parse_known_args()

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets', 'gallery'))
os.makedirs(out_dir, exist_ok=True)

Chart.set_theme(theme_name='vnstock', font_name='Inter', lang=args.lang)

def save_chart(fig, name):
    suffix = '_en' if args.lang == 'en' else ''
    fig.savefig(os.path.join(out_dir, f'{name}{suffix}.png'), bbox_inches='tight', dpi=150)
    plt.close(fig)

print(f"Đang tạo biểu đồ Summary Cards ({args.lang})...")

# Dữ liệu mô phỏng cho FPT
fpt_metrics_vi = {
    'Vốn hóa (Tỷ)': '145,200',
    'P/E': '20.5',
    'P/B': '4.8',
    'ROE': '26.5%',
    'ROA': '11.2%',
    'Khối lượng TB (10 phiên)': '3.5M'
}
fpt_metrics_en = {
    'Market Cap (B)': '145,200',
    'P/E': '20.5',
    'P/B': '4.8',
    'ROE': '26.5%',
    'ROA': '11.2%',
    'Avg Vol (10d)': '3.5M'
}

np.random.seed(42)
# Tạo chuỗi giá giả định tăng trưởng
sparkline_fpt = pd.Series(130000 + np.random.randn(30).cumsum() * 1000)

fig, ax = Chart.summary_card(
    ticker='WWW',
    company_name='WWW Global Solutions' if args.lang == 'en' else 'Công ty Cổ phần WWW',
    current_price=135000,
    price_change=3500,
    price_change_pct=2.65,
    metrics=fpt_metrics_en if args.lang == 'en' else fpt_metrics_vi,
    sparkline_data=sparkline_fpt,
    signal='Positive' if args.lang == 'en' else 'Tích cực'
)
save_chart(fig, '19_summary_card_positive')

# Dữ liệu mô phỏng cho XYZ (Giảm giá, Tín hiệu tiêu cực)
vic_metrics_vi = {
    'Vốn hóa (Tỷ)': '168,500',
    'P/E': '35.2',
    'P/B': '1.5',
    'ROE': '5.4%',
    'ROA': '1.2%',
    'Khối lượng TB (10 phiên)': '2.1M'
}
vic_metrics_en = {
    'Market Cap (B)': '168,500',
    'P/E': '35.2',
    'P/B': '1.5',
    'ROE': '5.4%',
    'ROA': '1.2%',
    'Avg Vol (10d)': '2.1M'
}

sparkline_vic = pd.Series(45000 - np.random.randn(30).cumsum() * 500)

fig, ax = Chart.summary_card(
    ticker='XYZ',
    company_name='XYZ Technologies Group' if args.lang == 'en' else 'Tập đoàn XYZ - Công ty CP',
    current_price=42500,
    price_change=-1200,
    price_change_pct=-2.74,
    metrics=vic_metrics_en if args.lang == 'en' else vic_metrics_vi,
    sparkline_data=sparkline_vic,
    signal='Negative' if args.lang == 'en' else 'Tiêu cực'
)
save_chart(fig, '20_summary_card_negative')
