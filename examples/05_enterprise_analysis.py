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

print(f"Đang tạo biểu đồ Enterprise Analysis ({args.lang})...")

# 14. Phân tích Cơ bản: Doanh thu & Biên lợi nhuận (Combo Chart)
quarters = ['Q1-23', 'Q2-23', 'Q3-23', 'Q4-23', 'Q1-24', 'Q2-24']
rev_label = 'Net Revenue' if args.lang == 'en' else 'Doanh thu thuần'
margin_label = 'Gross Margin (%)' if args.lang == 'en' else 'Biên LNG (%)'

revenue = pd.Series([1200, 1350, 1100, 1500, 1400, 1600], index=quarters, name=rev_label)
margin = pd.Series([15, 16.5, 14, 18, 17, 19.5], index=quarters, name=margin_label)

title_9 = 'Revenue & Gross Margin Analysis' if args.lang == 'en' else 'Phân tích Cơ bản: Doanh thu & Biên Lợi nhuận Gộp'
left_ylabel_9 = 'Bn VND' if args.lang == 'en' else 'Tỷ VNĐ'

fig, ax1, ax2 = Chart.combo(
    revenue, 
    margin, 
    title=title_9, 
    left_ylabel=left_ylabel_9, 
    right_ylabel=margin_label,
    color_palette=['#64B5F6', '#FFB74D']
)
save_chart(fig, '09_fundamental_combo')

# 15. So sánh Chỉ số Tài chính (ROE, ROA) - Grouped Bar Chart
banks = ['VCB', 'BID', 'CTG', 'MBB', 'TCB']
roe = [21.5, 18.2, 17.5, 23.4, 19.8]
roa = [2.1, 1.5, 1.4, 2.5, 2.8]

df_ratios = pd.DataFrame({'ROE (%)': roe, 'ROA (%)': roa}, index=banks)
title_17 = 'Profitability Ratios (ROE & ROA)' if args.lang == 'en' else 'So sánh Hiệu quả Sinh lời (ROE & ROA)'
ylabel_17 = 'Ratio (%)' if args.lang == 'en' else 'Tỷ lệ (%)'

fig, ax = Chart.bar(
    df_ratios,
    title=title_17,
    ylabel=ylabel_17,
    data_labels=True,
    data_label_format='{:.1f}',
    data_label_fontsize=9,
    show_legend=True,
    color_palette=['#64B5F6', '#FFB74D']
)
save_chart(fig, '17_financial_ratios')

# 16. Bảng Xếp hạng Cổ phiếu (Table)
cols_11_en = ['Ticker', 'RS Score', 'P/E', 'Signal']
cols_11_vi = ['Mã CK', 'RS Score', 'P/E', 'Tín hiệu']
signals_11_en = ['STRONG BUY', 'HOLD', 'BUY', 'BUY', 'WATCH']
signals_11_vi = ['MUA MẠNH', 'NẮM GIỮ', 'MUA', 'MUA', 'THEO DÕI']

top_stocks = pd.DataFrame({
    'Ticker' if args.lang == 'en' else 'Mã CK': ['ABC', 'VCB', 'HPG', 'SSI', 'MWG'],
    'RS Score': [95, 88, 85, 80, 78],
    'P/E': [20.5, 14.2, 12.0, 18.5, 30.1],
    'Signal' if args.lang == 'en' else 'Tín hiệu': signals_11_en if args.lang == 'en' else signals_11_vi
})

title_11 = 'Top Stock Signal Rankings' if args.lang == 'en' else 'Xếp hạng Tín hiệu Cổ phiếu Tích cực'

fig = Chart.table(
    top_stocks, 
    title=title_11,
    colWidths=[0.2, 0.2, 0.2, 0.3],
    figsize=(7, 4)
)
save_chart(fig, '11_stock_screening_table')

# 17. Phân tích Dòng tiền (Cash Flow) - Bar chart
years = ['2019', '2020', '2021', '2022', '2023']
cfo = pd.Series([500, 600, 800, 750, 900], index=years, name='CFO')
cfi = pd.Series([-300, -400, -200, -500, -600], index=years, name='CFI')
cff = pd.Series([100, -100, -300, 200, -100], index=years, name='CFF')

cols_18 = ['Operating', 'Investing', 'Financing'] if args.lang == 'en' else ['HĐ Kinh doanh', 'HĐ Đầu tư', 'HĐ Tài chính']
df_cf = pd.DataFrame({cols_18[0]: cfo, cols_18[1]: cfi, cols_18[2]: cff})

title_18 = 'Corporate Cash Flow Structure Analysis' if args.lang == 'en' else 'Phân tích Cấu trúc Dòng tiền Doanh nghiệp'
ylabel_18 = 'Bn VND' if args.lang == 'en' else 'Tỷ VNĐ'

fig, ax = Chart.bar(
    df_cf,
    title=title_18,
    ylabel=ylabel_18,
    stacked=True,
    data_labels=True,
    data_label_position='center',
    data_label_color='#ffffff',
    data_label_fontsize=9,
    show_yaxis=False,
    color_palette=['#66BB6A', '#E57373', '#FFB74D'],
    grid=True
)
ax.axhline(0, color='#94a3b8', linewidth=1.5)
save_chart(fig, '18_cash_flow_stacked')
