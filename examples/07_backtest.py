import sys
import os
import pandas as pd
import numpy as np
import argparse

# Add the parent directory to sys.path to import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vnstock_ezchart import Chart

# 1. Generate Mock Data
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=100, freq='B') # Business days

# Generate random walk for prices
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

# Moving Averages for overlays
ma20 = data['Close'].rolling(window=20).mean()
ma50 = data['Close'].rolling(window=50).mean()

# Generate some random trades
trades = [
    {'time': dates[10].strftime('%Y-%m-%d'), 'type': 'MUA', 'price': close_prices[10]},
    {'time': dates[30].strftime('%Y-%m-%d'), 'type': 'BAN', 'price': close_prices[30]},
    {'time': dates[45].strftime('%Y-%m-%d'), 'type': 'MUA', 'price': close_prices[45]},
    {'time': dates[60].strftime('%Y-%m-%d'), 'type': 'BAN', 'price': close_prices[60]},
    {'time': dates[80].strftime('%Y-%m-%d'), 'type': 'MUA', 'price': close_prices[80]},
]

trades_df = pd.DataFrame(trades)

# Generate Portfolio (Equity & Drawdown)
# Assume we start with 1,000,000 VND, equity goes up/down smoothly for demo
equity = np.linspace(1000000, 1200000, 100) + np.random.normal(0, 20000, 100)
equity = pd.Series(equity, index=dates)

# Calculate drawdown
running_max = equity.cummax()
drawdown = (equity - running_max) / running_max

portfolio = pd.DataFrame({
    'equity': equity,
    'drawdown': drawdown
}, index=dates)

# 2. Draw Backtest Chart
chart = Chart()

# Define overlays
overlays = [
    {'data': ma20, 'color': '#3b82f6', 'width': 1.5, 'alpha': 0.8}, # Blue
    {'data': ma50, 'color': '#f59e0b', 'width': 1.5, 'alpha': 0.8}  # Orange
]

# Ensure output directory exists
out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs', 'assets', 'gallery')
os.makedirs(out_dir, exist_ok=True)

def generate_backtest_chart(lang):
    # Configure global language
    chart.set_theme(lang=lang)
    
    save_path = os.path.join(out_dir, f'23_backtest_{lang}.png')
    print(f"Generating backtest chart ({lang})...")
    title = 'VN-Index: Backtest Strategy Results' if lang == 'en' else 'VN-Index: Kết quả Backtest Chiến lược'

    fig, axes = chart.backtest(
        data=data,
        trades=trades_df,
        portfolio=portfolio,
        overlays=overlays,
        title=title,
        figsize=(14, 12),
        volume=True,
        savefig=save_path,
        show=False
    )
    print(f"Chart saved to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate backtest charts.')
    parser.add_argument('--lang', type=str, default=None, choices=['vi', 'en'], help='Language for chart labels')
    args = parser.parse_args()

    if args.lang:
        generate_backtest_chart(args.lang)
    else:
        generate_backtest_chart('vi')
        generate_backtest_chart('en')
