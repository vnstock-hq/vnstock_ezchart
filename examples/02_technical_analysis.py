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

print(f"Đang tạo biểu đồ Technical Analysis ({args.lang})...")

np.random.seed(42)
dates_cs = pd.date_range('2023-08-01', periods=100, freq='B')
open_p = 100 + np.random.randn(100).cumsum()
high_p = open_p + np.random.rand(100) * 3
low_p = open_p - np.random.rand(100) * 3
close_p = open_p + np.random.randn(100)
volume_p = np.random.randint(500000, 5000000, 100)

data_cs = pd.DataFrame({'Open': open_p, 'High': high_p, 'Low': low_p, 'Close': close_p, 'Volume': volume_p}, index=dates_cs)
sma_20 = data_cs['Close'].rolling(20).mean()
sma_50 = data_cs['Close'].rolling(50).mean()

delta = data_cs['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs))

# 6. Candlestick with Indicators
title_6 = 'Technical Analysis: Candlestick, SMA20/50 & RSI' if args.lang == 'en' else 'Phân tích Kỹ thuật: Nến Nhật, SMA20/50 & RSI'
fig, axes = Chart.candle(
    data_cs, 
    title=title_6, 
    volume=True,
    overlays=[
        {'data': sma_20, 'color': '#FFB74D', 'width': 1.5},
        {'data': sma_50, 'color': '#64B5F6', 'width': 1.5}
    ],
    subplots=[{'data': rsi, 'color': '#BA68C8', 'ylabel': 'RSI (14)'}],
    figsize=(14, 8)
)
save_chart(fig, '06_candlestick_advanced')

# 13. Seasonality Boxplot
np.random.seed(42)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
returns_data = [np.random.normal(0.02, 0.05, 20) for _ in range(12)]
df_season = pd.DataFrame(returns_data).T
df_season.columns = months if args.lang == 'en' else ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12']

title_13 = 'Monthly Returns Seasonality (Boxplot)' if args.lang == 'en' else 'Tính Chu kỳ: Phân bổ Lợi nhuận theo Tháng (Boxplot)'
xlabel_13 = 'Month' if args.lang == 'en' else 'Tháng'
ylabel_13 = 'Returns (%)' if args.lang == 'en' else 'Tỷ suất lợi nhuận (%)'

fig, ax = Chart.boxplot(
    df_season, 
    title=title_13, 
    xlabel=xlabel_13, 
    ylabel=ylabel_13,
    ytick_format='{:.1%}',
    color_palette='vnstock'
)
save_chart(fig, '13_seasonality_boxplot')

