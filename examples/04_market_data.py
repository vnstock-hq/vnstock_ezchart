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

print(f"Đang tạo biểu đồ Market Data ({args.lang})...")

# 11. Phân phối Bước giá - Khối lượng (Volume Profile / Order Book)
prices = np.arange(20.0, 21.0, 0.05)
prices = [round(p, 2) for p in prices]
bid_volumes = np.random.randint(10000, 500000, len(prices)//2)
ask_volumes = np.random.randint(10000, 500000, len(prices) - len(prices)//2)
volumes = list(bid_volumes) + list(ask_volumes)

orderbook = pd.DataFrame({'Price' if args.lang == 'en' else 'Giá': prices, 'Volume' if args.lang == 'en' else 'Khối lượng': volumes})
orderbook.set_index('Price' if args.lang == 'en' else 'Giá', inplace=True)

colors = ['#66BB6A' if i < len(bid_volumes) else '#E57373' for i in range(len(prices))]

title_11 = 'Order Book / Volume Profile' if args.lang == 'en' else 'Bước giá - Khối lượng (Order Book / Volume Profile)'
xlabel_11 = 'Price Level (VND)' if args.lang == 'en' else 'Mức giá (VND)'
ylabel_11 = 'Pending Volume' if args.lang == 'en' else 'Khối lượng chờ khớp'

fig, ax = Chart.bar(
    orderbook['Volume' if args.lang == 'en' else 'Khối lượng'],
    title=title_11,
    xlabel=xlabel_11,
    ylabel=ylabel_11,
    color_palette=colors,
    ytick_format='{:.0f}',
    grid=True,
    grid_axis='y',
    tick_rotation=45
)
save_chart(fig, '15_orderbook_volume')

# 12. Giao dịch Khối Ngoại (Foreign Trade)
dates = pd.date_range('2023-10-01', periods=30, freq='B')
net_value = np.random.uniform(-500, 800, 30) # Tỷ VNĐ
foreign_trade = pd.Series(net_value, index=dates.strftime('%d/%m'))

colors_ft = ['#66BB6A' if v > 0 else '#E57373' for v in net_value]
title_12 = 'Net Foreign Trade Flow' if args.lang == 'en' else 'Dòng tiền Khối Ngoại (Net Foreign Trade)'
xlabel_12 = 'Trading Day' if args.lang == 'en' else 'Ngày giao dịch'
ylabel_12 = 'Net Buy Value (Bn VND)' if args.lang == 'en' else 'Giá trị mua ròng (Tỷ VNĐ)'

fig, ax = Chart.bar(
    foreign_trade,
    title=title_12,
    xlabel=xlabel_12,
    ylabel=ylabel_12,
    color_palette=colors_ft,
    grid=True,
    grid_axis='y',
    tick_rotation=90
)

# Reduce X ticks
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::3])
ax.xaxis.set_ticklabels(ticklabels[::3])

save_chart(fig, '16_foreign_trade')

# 13. Market Sentiment Wordcloud
sentiment_text_en = "BUY STRONG GROWTH PROFIT BREAKOUT CASHFLOW SUPPORT SSI BULLISH HPG FOREIGN NET_BUY VOLUME LIQUIDITY"
sentiment_text_vi = "FPT MUA VCB MẠNH TĂNG_TRƯỞNG LỢI_NHUẬN ĐỘT_PHÁ DÒNG_TIỀN HỖ_TRỢ SSI BÙNG_NỔ HPG KHỐI_NGOẠI GOM VIX THANH_KHOẢN"

title_13 = 'Market Sentiment' if args.lang == 'en' else 'Tâm lý Thị trường (Market Sentiment)'

fig, ax = Chart.wordcloud(
    sentiment_text_en if args.lang == 'en' else sentiment_text_vi, 
    title=title_13, 
    max_words=30,
    color_palette='trend',
    show=False
)
save_chart(fig, '12_sentiment_wordcloud')
