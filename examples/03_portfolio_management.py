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

print(f"Đang tạo biểu đồ Portfolio Management ({args.lang})...")

np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=1000, freq='B')
df_returns = pd.Series(np.random.normal(0.0006, 0.015, 1000), index=dates, name='Strategy' if args.lang == 'en' else 'Chiến lược')
df_bench = pd.Series(np.random.normal(0.0004, 0.012, 1000), index=dates, name='VN-Index')

# 7. Portfolio Treemap
tickers = ['VCB', 'BID', 'CTG', 'VPB', 'TCB', 'MBB', 'ACB', 'STB', 'HDB', 'VIB']
weights = [25, 15, 12, 10, 8, 8, 7, 5, 5, 5]
title_7 = 'Portfolio Allocation (Top 10 Stocks)' if args.lang == 'en' else 'Phân bổ Tỷ trọng Danh mục (Top 10 Cổ phiếu)'
fig, ax = Chart.treemap(
    values=weights, 
    labels=tickers, 
    title=title_7,
    color_palette='flatui'
)
save_chart(fig, '07_portfolio_treemap')

# 8. Scatter Correlation
df_scatter = pd.DataFrame({'Strategy': df_returns, 'Benchmark': df_bench})
title_8 = 'Beta & Correlation: Strategy vs VN-Index' if args.lang == 'en' else 'Beta & Tương quan: Chiến lược vs VN-Index'
xlabel_8 = 'VN-Index Returns' if args.lang == 'en' else 'Lợi nhuận VN-Index'
ylabel_8 = 'Strategy Returns' if args.lang == 'en' else 'Lợi nhuận Chiến lược'
fig, ax = Chart.scatter(
    df_scatter, 
    x='Benchmark', 
    y='Strategy', 
    title=title_8, 
    xlabel=xlabel_8, 
    ylabel=ylabel_8,
    alpha=0.5,
    xtick_format='{:.1%}',
    ytick_format='{:.1%}',
    color_palette=['#BA68C8']
)
m, b = np.polyfit(df_scatter['Benchmark'].dropna(), df_scatter['Strategy'].dropna(), 1)
ax.plot(df_scatter['Benchmark'], m*df_scatter['Benchmark'] + b, color='#E57373', linewidth=2)
save_chart(fig, '08_correlation_scatter')

# 9. Multi-Asset Line
labels_9 = ['Stocks', 'Bonds', 'Gold'] if args.lang == 'en' else ['Cổ phiếu', 'Trái phiếu', 'Vàng']
multi_assets = pd.DataFrame({
    labels_9[0]: np.random.normal(0.0006, 0.015, 500),
    labels_9[1]: np.random.normal(0.0002, 0.002, 500),
    labels_9[2]: np.random.normal(0.0003, 0.008, 500)
}, index=pd.date_range('2022-01-01', periods=500)).cumsum() * 100

title_9 = 'Multi-Asset Class Growth' if args.lang == 'en' else 'Tăng trưởng Đa lớp Tài sản (Multi-Asset Class Growth)'
ylabel_9 = 'Cumulative Value (%)' if args.lang == 'en' else 'Giá trị Tích lũy (%)'
legend_title_9 = 'Asset Class' if args.lang == 'en' else 'Lớp tài sản'

fig, ax = Chart.line(
    multi_assets, 
    title=title_9,
    ylabel=ylabel_9,
    grid=True,
    show_legend=True,
    legend_title=legend_title_9,
    color_palette=['#66BB6A', '#90A4AE', '#FFB74D']
)
save_chart(fig, '10_multi_asset_line')

# 10. Pairplot
cols_10 = ['Banking', 'Securities', 'Real Estate'] if args.lang == 'en' else ['Ngân hàng', 'Chứng khoán', 'Bất động sản']
sectors = pd.DataFrame({
    cols_10[0]: np.random.randn(200),
    cols_10[1]: np.random.randn(200) + 0.5 * np.random.randn(200),
    cols_10[2]: np.random.randn(200) - 0.2 * np.random.randn(200)
})
g = Chart.pairplot(
    sectors, 
    diag_kind='kde',
    corner=True,
    plot_kws={'alpha': 0.6, 'color': '#BA68C8'},
    diag_kws={'color': '#66BB6A'}
)
title_10 = 'Sector Returns Correlation' if args.lang == 'en' else 'Tương quan Lợi nhuận giữa các Nhóm ngành'
g.figure.suptitle(title_10, y=1.02, fontweight="black", fontsize=16)
save_chart(g.figure, '14_sectors_pairplot')
