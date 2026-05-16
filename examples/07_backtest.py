import sys
import os
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
c1 = theme_colors[0]
c2 = theme_colors[1 % len(theme_colors)]

def save_chart(fig, name):
    fig.savefig(os.path.join(out_dir, f'{name}.png'), bbox_inches='tight', dpi=150)
    plt.close(fig)

# 1. Generate Mock Data
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=100, freq='B')

price_changes = np.random.normal(loc=0.001, scale=0.02, size=100)
close_prices = 100 * np.exp(np.cumsum(price_changes))
high_prices = close_prices * (1 + np.abs(np.random.normal(0, 0.01, size=100)))
low_prices = close_prices * (1 - np.abs(np.random.normal(0, 0.01, size=100)))
open_prices = close_prices * (1 + np.random.normal(0, 0.005, size=100))
volumes = np.random.randint(100000, 5000000, size=100)

data = pd.DataFrame({
    'Open': open_prices,
    'High': high_prices,
    'Low': low_prices,
    'Close': close_prices,
    'Volume': volumes
}, index=dates)

ma20 = data['Close'].rolling(window=20).mean()
ma50 = data['Close'].rolling(window=50).mean()

trades = [
    {'time': dates[10].strftime('%Y-%m-%d'), 'type': 'MUA', 'price': close_prices[10]},
    {'time': dates[30].strftime('%Y-%m-%d'), 'type': 'BAN', 'price': close_prices[30]},
    {'time': dates[45].strftime('%Y-%m-%d'), 'type': 'MUA', 'price': close_prices[45]},
    {'time': dates[60].strftime('%Y-%m-%d'), 'type': 'BAN', 'price': close_prices[60]},
    {'time': dates[80].strftime('%Y-%m-%d'), 'type': 'MUA', 'price': close_prices[80]},
]

trades_df = pd.DataFrame(trades)

equity = np.linspace(1000000, 1200000, 100) + np.random.normal(0, 20000, 100)
equity = pd.Series(equity, index=dates)

running_max = equity.cummax()
drawdown = (equity - running_max) / running_max

portfolio = pd.DataFrame({
    'equity': equity,
    'drawdown': drawdown
}, index=dates)

# 2. Draw Backtest Chart
chart = Chart()

overlays = [
    {'data': ma20, 'color': c1, 'width': 1.5, 'alpha': 0.8},
    {'data': ma50, 'color': c2, 'width': 1.5, 'alpha': 0.8}
]

print(f"Generating backtest chart ({args.lang})...")
title = 'VN-Index: Backtest Strategy Results' if args.lang == 'en' else 'VN-Index: Kết quả Backtest Chiến lược'

fig, axes = chart.backtest(
    data=data,
    trades=trades_df,
    portfolio=portfolio,
    overlays=overlays,
    title=title,
    figsize=(14, 12),
    volume=True,
    show=False
)
save_chart(fig, '23_backtest')

print("Hoàn tất!")
