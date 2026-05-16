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
parser.add_argument('--theme', type=str, default='vnstock', choices=['vnstock', 'academic', 'minimal', 'flatui'])
args, _ = parser.parse_known_args()

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets', 'gallery', args.theme, args.lang))
os.makedirs(out_dir, exist_ok=True)

Chart.set_theme(theme_name=args.theme, font_name='Inter', lang=args.lang)

from vnstock_ezchart.utils import Utils
theme_colors = Utils.brand_palettes[args.theme]
c_pos = theme_colors[0]
c_neg = theme_colors[3] if len(theme_colors) > 3 else theme_colors[1]
c_accent = theme_colors[2] if len(theme_colors) > 2 else theme_colors[0]

def save_chart(fig, name):
    fig.savefig(os.path.join(out_dir, f'{name}.png'), bbox_inches='tight', dpi=150)
    plt.close(fig)

print(f"Đang tạo biểu đồ Performance & Risk ({args.lang})...")

# Mock Data
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=1000, freq='B')
returns_strategy = np.random.normal(0.0006, 0.015, 1000)
returns_benchmark = np.random.normal(0.0004, 0.012, 1000)

df_returns = pd.Series(returns_strategy, index=dates, name='Strategy' if args.lang == 'en' else 'Chiến lược')
df_bench = pd.Series(returns_benchmark, index=dates, name='VN-Index')
cum_returns = (1 + df_returns).cumprod() - 1
cum_bench = (1 + df_bench).cumprod() - 1

# 1. Equity Curve
title_1 = 'Portfolio vs VN-Index Performance (Equity Curve & Drawdown)' if args.lang == 'en' else 'Hiệu suất Danh mục vs VN-Index (Equity Curve & Drawdown)'
fig, ax1, ax2 = Chart.equity_curve(
    cum_returns, 
    benchmark=cum_bench, 
    title=title_1,
    figsize=(12, 7)
)
save_chart(fig, '01_equity_curve')

# 2. Returns Heatmap
title_2 = 'Seasonality Analysis: Monthly Returns Matrix' if args.lang == 'en' else 'Phân tích Tính Chu Kỳ: Ma trận Lợi nhuận Hàng tháng'
fig, ax = Chart.returns_heatmap(
    df_returns, 
    title=title_2,
    figsize=(10, 5)
)
save_chart(fig, '02_returns_heatmap')

# 3. Yearly Returns
yearly_returns = df_returns.resample('YE').apply(lambda x: (1 + x).prod() - 1)
yearly_returns.index = yearly_returns.index.year
title_3 = 'Yearly Performance' if args.lang == 'en' else 'Tỷ suất lợi nhuận qua các năm'
xlabel_3 = 'Year' if args.lang == 'en' else 'Năm'
fig, ax = Chart.bar(
    yearly_returns, 
    title=title_3, 
    xlabel=xlabel_3, 
    data_labels=True, 
    data_label_format='{:.1%}',
    show_yaxis=False, 
    color_palette=[c_pos if v > 0 else c_neg for v in yearly_returns.values]
)
save_chart(fig, '03_yearly_returns')

# 4. Rolling Volatility
rolling_vol = df_returns.rolling(window=30).std() * np.sqrt(252)
title_4 = 'Risk Management: Rolling Volatility (30-day)' if args.lang == 'en' else 'Quản trị Rủi ro: Độ biến động (Rolling Volatility 30-ngày)'
ylabel_4 = 'Volatility (Annualized)' if args.lang == 'en' else 'Độ biến động (Hàng năm)'
fig, ax = Chart.line(
    rolling_vol, 
    title=title_4,
    ylabel=ylabel_4,
    color_palette=[c_neg],
    ytick_format='{:.1%}',
    grid=True
)
save_chart(fig, '04_rolling_volatility')

# 5. Returns Distribution
title_5 = 'Daily Returns Distribution' if args.lang == 'en' else 'Phân phối Lợi nhuận hàng ngày (Daily Returns Distribution)'
xlabel_5 = 'Returns' if args.lang == 'en' else 'Lợi nhuận'
ylabel_5 = 'Frequency' if args.lang == 'en' else 'Tần suất'
fig, ax = Chart.hist(
    df_returns, 
    title=title_5, 
    xlabel=xlabel_5, 
    ylabel=ylabel_5, 
    bins=50, 
    xtick_format='{:.1%}',
    color_palette=[c_pos]
)
ax.axvline(x=0, color=c_accent, linestyle='--', linewidth=1.5)
save_chart(fig, '05_returns_distribution')

# 6. Seasonality Boxplot
np.random.seed(42)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
returns_data = [np.random.normal(0.02, 0.05, 20) for _ in range(12)]
df_season = pd.DataFrame(returns_data).T
df_season.columns = months if args.lang == 'en' else ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']

title_6 = 'Monthly Returns Seasonality (Boxplot)' if args.lang == 'en' else 'Tính Chu kỳ: Phân bổ Lợi nhuận theo Tháng (Boxplot)'
xlabel_6 = 'Month' if args.lang == 'en' else 'Tháng'
ylabel_6 = 'Returns (%)' if args.lang == 'en' else 'Tỷ suất lợi nhuận (%)'

fig, ax = Chart.boxplot(
    df_season, 
    title=title_6, 
    xlabel=xlabel_6, 
    ylabel=ylabel_6,
    ytick_format='{:.1%}',
    show=False
)
save_chart(fig, '13_seasonality_boxplot')
