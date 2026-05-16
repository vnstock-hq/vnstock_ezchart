import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vnstock.api.quote import Quote
from vnstock_ta.interface import Indicator
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
c3 = theme_colors[2 % len(theme_colors)]
c4 = theme_colors[3 % len(theme_colors)]
c5 = theme_colors[4 % len(theme_colors)]
c_pos = theme_colors[0]
c_neg = theme_colors[3] if len(theme_colors) > 3 else theme_colors[1]

def save_chart(fig, name):
    fig.savefig(os.path.join(out_dir, f'{name}.png'), bbox_inches='tight', dpi=150)
    plt.close(fig)

print(f"Đang tạo biểu đồ Technical Analysis ({args.lang})...")

# --- 1. Basic Technical Analysis (Candlestick + SMA/RSI) ---
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

title_6 = 'Technical Analysis: Candlestick, SMA20/50 & RSI' if args.lang == 'en' else 'Phân tích Kỹ thuật: Nến Nhật, SMA20/50 & RSI'
fig, axes = Chart.candle(
    data_cs, 
    title=title_6, 
    volume=True,
    overlays=[
        {'data': sma_20, 'color': c2, 'width': 1.5},
        {'data': sma_50, 'color': c3, 'width': 1.5}
    ],
    subplots=[{'data': rsi, 'color': c4, 'ylabel': 'RSI (14)'}],
    figsize=(14, 8),
    show=False
)
save_chart(fig, '06_candlestick_advanced')

# --- 2. Advanced Technical Indicators (vnstock_ta) ---
def get_data(ticker):
    q = Quote(symbol=ticker, source='VCI')
    df = q.history(start='2023-01-01', end='2026-05-14', interval='1D')
    if 'time' in df.columns:
        df = df.set_index('time')
        df.index = pd.to_datetime(df.index)
    return df

print("Fetching data for FPT to generate indicators...")
df = get_data('FPT')
df_plot = df.iloc[-150:]
ta = Indicator(df)
price_mean = df_plot['close'].mean()

indicators_to_plot = [
    ('trend', 'ichimoku'),
    ('trend', 'supertrend'),
    ('momentum', 'macd'),
    ('momentum', 'stochrsi'),
    ('volatility', 'bbands'),
    ('volatility', 'donchian')
]

for category, method_name in indicators_to_plot:
    module = getattr(ta, category)
    try:
        method = getattr(module, method_name)
        result = method()
        
        if result is None or (isinstance(result, pd.DataFrame) and result.empty) or (isinstance(result, pd.Series) and result.empty):
            continue
            
        if isinstance(result, tuple):
            result = result[0]
            
        if isinstance(result, pd.Series):
            result = result.to_frame(name=method_name.upper())
            
        result = result.reindex(df_plot.index)
        
        overlays = []
        subplots = []
        fill_between = None
        legend_labels = []
        overlay_legend = []
        
        if '_' in method_name:
            display_name = method_name.replace('_', ' ').title()
        else:
            display_name = method_name.upper()
            
        title_prefix = 'Indicator' if args.lang == 'en' else 'Chỉ báo'
        title = f"{title_prefix}: {category.capitalize()} - {display_name}"
        
        if method_name == 'macd':
            macd_line = result.iloc[:, 0]
            macd_hist = result.iloc[:, 1]
            macd_signal = result.iloc[:, 2]
            colors = [c_pos if val >= 0 else c_neg for val in macd_hist]
            subplots = [[
                {"data": macd_hist, "type": "bar", "color": colors, "ylabel": "MACD"},
                {"data": macd_line, "color": c1, "width": 1.5},
                {"data": macd_signal, "color": c2, "width": 1.5}
            ]]
            legend_labels = ["Histogram", "MACD Line", "Signal Line"]
        
        elif method_name in ['rsi', 'stoch', 'cmo', 'roc', 'willr', 'stochrsi']:
            subplot_group = []
            for i, col in enumerate(result.columns):
                item = {"data": result[col], "color": [c1, c2, c3, c4][i%4]}
                if i == 0:
                    item["ylabel"] = display_name
                subplot_group.append(item)
                if method_name in ['stoch']:
                    legend_labels.append(col)
            
            if method_name == 'rsi':
                subplot_group.append({"data": pd.Series(70, index=df_plot.index), "color": c_neg, "linestyle": "dashed", "alpha": 0.5})
                subplot_group.append({"data": pd.Series(30, index=df_plot.index), "color": c_pos, "linestyle": "dashed", "alpha": 0.5})
            elif method_name == 'stoch':
                subplot_group.append({"data": pd.Series(80, index=df_plot.index), "color": c_neg, "linestyle": "dashed", "alpha": 0.5})
                subplot_group.append({"data": pd.Series(20, index=df_plot.index), "color": c_pos, "linestyle": "dashed", "alpha": 0.5})
            elif method_name == 'willr':
                subplot_group.append({"data": pd.Series(-20, index=df_plot.index), "color": c_neg, "linestyle": "dashed", "alpha": 0.5})
                subplot_group.append({"data": pd.Series(-80, index=df_plot.index), "color": c_pos, "linestyle": "dashed", "alpha": 0.5})
            elif method_name == 'stochrsi':
                subplot_group.append({"data": pd.Series(80, index=df_plot.index), "color": c_neg, "linestyle": "dashed", "alpha": 0.5})
                subplot_group.append({"data": pd.Series(20, index=df_plot.index), "color": c_pos, "linestyle": "dashed", "alpha": 0.5})
            
            subplots = [subplot_group]
            
        elif method_name == 'adx':
            adx_col = [c for c in result.columns if c.startswith('ADX_')][0]
            subplots = [[{"data": result[adx_col], "color": c1, "ylabel": display_name, "width": 1.5}]]
            
        elif method_name == 'pvo':
            pvo_col = [c for c in result.columns if c.startswith('PVO_')][0]
            subplots = [[{"data": result[pvo_col], "color": c1, "ylabel": display_name, "width": 1.5}]]

        elif method_name == 'pivots':
            pivot_colors = [c1, c2, c3, c4, c5]
            for i, col in enumerate(result.columns):
                overlays.append({"data": result[col], "color": pivot_colors[i % len(pivot_colors)], "width": 1.0, "alpha": 0.3})
                overlay_legend.append(col)
            
        elif method_name in ['hl2', 'hlc3', 'ohlc4', 'midprice']:
            for col in result.columns:
                overlays.append({"data": result[col], "color": c1, "alpha": 0.5, "width": 1.5})
                
        elif method_name == 'ichimoku':
            isa, isb, its, iks = result['ISA_9'], result['ISB_26'], result['ITS_9'], result['IKS_26']
            overlays = [
                {"data": its, "color": c1},
                {"data": iks, "color": c_neg}
            ]
            fill_between = [
                dict(y1=isa.values, y2=isb.values, where=isa.values >= isb.values, color=c_pos, alpha=0.3),
                dict(y1=isa.values, y2=isb.values, where=isa.values < isb.values, color=c_neg, alpha=0.3)
            ]
            
        elif method_name == 'psar':
            for col in result.columns:
                if col.startswith('PSARl_'):
                    overlays.append({"data": result[col], "color": c_pos, "type": "scatter", "markersize": 15})
                elif col.startswith('PSARs_'):
                    overlays.append({"data": result[col], "color": c_neg, "type": "scatter", "markersize": 15})
                    
        elif method_name == 'supertrend':
            long_col = [c for c in result.columns if c.startswith('SUPERTl_')][0]
            short_col = [c for c in result.columns if c.startswith('SUPERTs_')][0]
            overlays.append({"data": result[long_col], "color": c_pos, "width": 2.5})
            overlays.append({"data": result[short_col], "color": c_neg, "width": 2.5})
            
        elif method_name == 'bbands':
            bbl, bbm, bbu = result.iloc[:, 0], result.iloc[:, 1], result.iloc[:, 2]
            overlays = [{"data": bbm, "color": c2, "width": 1.5}]
            fill_between = dict(y1=bbu.values, y2=bbl.values, color=c1, alpha=0.15)
            
        elif method_name == 'donchian':
            dcl, dcm, dcu = result.iloc[:, 0], result.iloc[:, 1], result.iloc[:, 2]
            overlays = [
                {"data": dcm, "color": c2, "width": 1.5, "alpha": 0.8},
                {"data": dcu, "color": c1, "width": 1.0, "alpha": 0.5},
                {"data": dcl, "color": c1, "width": 1.0, "alpha": 0.5}
            ]
            fill_between = dict(y1=dcu.values, y2=dcl.values, color=c1, alpha=0.1)
            overlay_legend = ["Mid", "Upper", "Lower"]
            
        elif method_name == 'kc':
            kcl, kcb, kcu = result.iloc[:, 0], result.iloc[:, 1], result.iloc[:, 2]
            overlays = [{"data": kcb, "color": c2, "width": 1.5}]
            fill_between = dict(y1=kcu.values, y2=kcl.values, color=c1, alpha=0.15)
            
        else:
            subplot_group = []
            colors = [c1, c_neg, c_pos, c2, c3]
            for i, col in enumerate(result.columns):
                series = result[col]
                color = colors[i % len(colors)]
                s_mean = series.abs().mean()
                if pd.isna(s_mean) or s_mean == 0:
                    continue
                is_overlay = 0.5 < (s_mean / price_mean) < 2.0 and series.min() >= 0
                if is_overlay:
                    overlays.append({"data": series, "color": color, "width": 1.5})
                else:
                    item = {"data": series, "color": color}
                    if len(subplot_group) == 0:
                        item["ylabel"] = display_name
                    subplot_group.append(item)
                    legend_labels.append(col)
                    
            if subplot_group:
                subplots = [subplot_group]

        # Generate Chart
        if fill_between is not None:
            fig, axes = Chart.candle(df_plot, title=title, figsize=(12, 8), overlays=overlays, subplots=subplots, fill_between=fill_between, show=False)
        else:
            fig, axes = Chart.candle(df_plot, title=title, figsize=(12, 8), overlays=overlays, subplots=subplots, show=False)
        
        if subplots and len(legend_labels) > 1 and len(axes) > 4:
            if len(legend_labels) > 6:
                legend_labels = legend_labels[:6]
            axes[4].legend(legend_labels, loc="upper left", fontsize=8, framealpha=0.6)
            
        if overlays and len(overlay_legend) > 0 and len(axes) > 0:
            if len(overlay_legend) > 6:
                overlay_legend = overlay_legend[:6]
            axes[0].legend(overlay_legend, loc="upper left", fontsize=8, framealpha=0.6)

        save_path = f"indicator_{category}_{method_name}"
        save_chart(fig, save_path)
        
    except Exception as e:
        print(f"  -> Error calculating/plotting {method_name}: {e}")

print("Hoàn tất!")
