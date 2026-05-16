import os
from typing import Union, List, Optional, Tuple, Dict, Any
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.ticker as mticker
from ..utils import Utils

class QuantMixin:
    @classmethod
    def backtest(
        cls, 
        data: pd.DataFrame, 
        trades: Union[pd.DataFrame, List[Dict[str, Any]], np.ndarray, None] = None, 
        portfolio: pd.DataFrame = None, 
        title: str = 'Backtest Results', 
        figsize: Tuple[float, float] = (14, 10), 
        volume: bool = True,
        overlays: list = None,
        **kwargs
    ) -> Tuple['plt.Figure', 'plt.Axes']:
        """
        Draws a comprehensive backtest chart including candlesticks, trades, volume, equity curve, and drawdown.

        Args:
            data (pd.DataFrame): Stock price data with DatetimeIndex and columns ['Open', 'High', 'Low', 'Close', 'Volume'].
            trades (pd.DataFrame, list, np.ndarray): Trade data. If DataFrame, should contain ['time', 'type', 'price'] 
                                                     where type is 'MUA'/'Buy' or 'BAN'/'Sell'.
            portfolio (pd.DataFrame): Portfolio performance with DatetimeIndex and columns ['equity', 'drawdown'].
            title (str): Chart title.
            figsize (tuple): Chart size.
            volume (bool): Show volume panel.
            overlays (list): Additional indicators for the main candlestick panel.
            **kwargs: Styling parameters.
        """
        palette_name = kwargs.pop('color_palette', cls._global_theme)
        palette = Utils.brand_palettes.get(palette_name, Utils.brand_palettes['vnstock'])
        
        # Soft Premium Colors
        up_color = palette[0] if len(palette) > 0 else '#4CAF50'
        down_color = palette[3] if len(palette) > 3 else '#EF5350'
        grid_color = '#f1f5f9'
        bg_color = '#ffffff'
        text_color = '#475569'
        
        buy_color = up_color
        sell_color = down_color
        equity_color = palette[1] if len(palette) > 1 else '#3b82f6'
        drawdown_color = palette[3] if len(palette) > 3 else '#ef4444'

        mc = mpf.make_marketcolors(
            up=up_color, down=down_color, edge='inherit', wick='inherit', volume='in', ohlc='inherit'
        )
    
        s = mpf.make_mpf_style(
            marketcolors=mc, gridstyle='-', gridcolor=grid_color, facecolor=bg_color,
            edgecolor=bg_color, figcolor=bg_color, y_on_right=False,
            rc={
                'patch.edgecolor': '#FFFFFF', 'patch.force_edgecolor': True, 'patch.linewidth': 1.0,
                'axes.labelsize': 12, 'axes.labelcolor': text_color,
                'xtick.color': text_color, 'ytick.color': text_color,
                'axes.edgecolor': '#cbd5e1',
            }
        )
    
        # 1. Process Main Data
        plot_df = data.copy()
        if not isinstance(plot_df.index, pd.DatetimeIndex):
            if 'time' in plot_df.columns:
                plot_df = plot_df.set_index('time')
            elif 'date' in plot_df.columns:
                plot_df = plot_df.set_index('date')
            plot_df.index = pd.to_datetime(plot_df.index)
        
        rename_map = {c: c.capitalize() for c in plot_df.columns if c.lower() in ['open', 'high', 'low', 'close', 'volume']}
        plot_df = plot_df.rename(columns=rename_map)

        # 2. Process Trades
        buy_markers = pd.Series(index=plot_df.index, dtype=float)
        sell_markers = pd.Series(index=plot_df.index, dtype=float)

        if trades is not None:
            if isinstance(trades, pd.DataFrame):
                tr_df = trades.copy()
            elif isinstance(trades, list):
                tr_df = pd.DataFrame(trades)
            elif isinstance(trades, np.ndarray):
                # Attempt to convert to dataframe assuming structured array or record array
                try:
                    tr_df = pd.DataFrame(trades)
                except:
                    tr_df = pd.DataFrame()
            else:
                tr_df = pd.DataFrame()

            if not tr_df.empty:
                # Find time column
                time_col = next((c for c in tr_df.columns if str(c).lower() in ['time', 'date', 'trade_date']), None)
                type_col = next((c for c in tr_df.columns if str(c).lower() in ['type', 'trade_type', 'side']), None)
                price_col = next((c for c in tr_df.columns if str(c).lower() in ['price', 'exec_price']), None)

                if time_col and type_col and price_col:
                    tr_df[time_col] = pd.to_datetime(tr_df[time_col])
                    for _, row in tr_df.iterrows():
                        t_date = row[time_col]
                        t_type = str(row[type_col]).upper()
                        t_price = float(row[price_col])

                        if pd.notna(t_date) and t_date in plot_df.index:
                            if t_type in ['MUA', 'BUY', 'LONG', '1', '1.0']:
                                buy_markers.loc[t_date] = t_price * 0.98 # Place below low
                            elif t_type in ['BAN', 'SELL', 'SHORT', '-1', '-1.0']:
                                sell_markers.loc[t_date] = t_price * 1.02 # Place above high

        # 3. Process Portfolio (Equity & Drawdown)
        equity_series = None
        drawdown_series = None
        if portfolio is not None:
            port_df = portfolio.copy()
            if not isinstance(port_df.index, pd.DatetimeIndex):
                time_col = next((c for c in port_df.columns if str(c).lower() in ['time', 'date']), None)
                if time_col:
                    port_df = port_df.set_index(time_col)
                port_df.index = pd.to_datetime(port_df.index)
            
            # Reindex to match plot_df
            port_df = port_df.reindex(plot_df.index).ffill()
            
            eq_col = next((c for c in port_df.columns if str(c).lower() in ['equity', 'portfolio_value', 'capital', 'cumulative_return', 'return']), None)
            dd_col = next((c for c in port_df.columns if str(c).lower() in ['drawdown', 'dd']), None)

            if eq_col:
                equity_series = port_df[eq_col]
            if dd_col:
                drawdown_series = port_df[dd_col]

        # 4. Construct AddPlots
        apds = []
        
        # Overlays
        if overlays:
            for overlay in overlays:
                if isinstance(overlay, dict):
                    apds.append(mpf.make_addplot(overlay['data'], type=overlay.get('type', 'line'), color=overlay.get('color', None), panel=0, alpha=overlay.get('alpha', 0.8), width=overlay.get('width', 1.0)))
                else:
                    apds.append(mpf.make_addplot(overlay, type='line', panel=0, alpha=0.8, width=1.0))

        # Trade Markers
        if not buy_markers.isna().all():
            apds.append(mpf.make_addplot(buy_markers, type='scatter', markersize=150, marker='^', color=buy_color, panel=0))
        if not sell_markers.isna().all():
            apds.append(mpf.make_addplot(sell_markers, type='scatter', markersize=150, marker='v', color=sell_color, panel=0))

        # Determine Panel Layout
        panel_idx = 1 if volume else 0
        if volume:
            panel_idx = 1
        else:
            panel_idx = 0
            
        panel_ratios = [5]
        if volume:
            panel_ratios.append(1)

        eq_panel = None
        if equity_series is not None:
            panel_idx += 1
            eq_panel = panel_idx
            apds.append(mpf.make_addplot(equity_series, type='line', color=equity_color, panel=eq_panel, width=1.5, ylabel='Equity'))
            panel_ratios.append(1.5)

        dd_panel = None
        if drawdown_series is not None:
            panel_idx += 1
            dd_panel = panel_idx
            # We use line here, and will fill_between in post-processing
            apds.append(mpf.make_addplot(drawdown_series, type='line', color=drawdown_color, panel=dd_panel, width=1.0, ylabel='Drawdown'))
            panel_ratios.append(1)

        font_name = kwargs.pop('font_name', plt.rcParams['font.family'])
        if isinstance(font_name, list):
            font_name = font_name[0]

        # 5. Plot!
        savefig_kwargs = kwargs.pop('savefig', None)
        show_kwargs = kwargs.pop('show', True)
        
        plot_kwargs = {
            'type': 'candle',
            'volume': volume,
            'style': s,
            'figsize': figsize,
            'title': "",
            'ylabel': 'Giá',
            'ylabel_lower': 'Khối lượng' if volume else '',
            'returnfig': True,
            'tight_layout': True,
            'xrotation': 0
        }
        
        if apds:
            plot_kwargs['addplot'] = apds
        if len(panel_ratios) > 1:
            plot_kwargs['panel_ratios'] = panel_ratios
            
        plot_kwargs.update(kwargs)
        
        fig, axes = mpf.plot(plot_df, **plot_kwargs)

        # 6. Post-processing styling
        if title:
            fig.suptitle(title, y=1.02, fontweight="black", fontname=font_name, fontsize=16, color='#111827')

        # Volume formatter
        def format_volume(x, pos):
            if x >= 1e6: return f'{x*1e-6:.1f}M'
            elif x >= 1e3: return f'{x*1e-3:.0f}K'
            return f'{x:.0f}'
        
        # Soft spines and custom labels
        for ax in axes:
            ylabel = ax.get_ylabel()
            
            # Fix Volume Formatting
            if 'Khối lượng' in ylabel or 'Volume' in ylabel:
                clean_label = 'Khối lượng' if 'Khối lượng' in ylabel else 'Volume'
                ax.set_ylabel(clean_label, fontsize=12, fontweight='medium', color=text_color, labelpad=10)
                ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_volume))
                if hasattr(ax.yaxis, 'offsetText'):
                    ax.yaxis.offsetText.set_visible(False)
                for patch in ax.patches:
                    patch.set_edgecolor('#FFFFFF')
                    patch.set_linewidth(0.5)
            elif ylabel:
                ax.set_ylabel(ylabel, fontsize=12, fontweight='medium', color=text_color, labelpad=10)

            # Fill Drawdown Panel
            if 'Drawdown' in ylabel and drawdown_series is not None:
                # mplfinance axes have the index mapping as x-coordinates (0, 1, 2, ...)
                x_vals = np.arange(len(plot_df))
                ax.fill_between(x_vals, drawdown_series.values, 0, color=drawdown_color, alpha=0.2)
                # Format y-axis as percentage if values are decimals
                if drawdown_series.min() > -10.0 and drawdown_series.max() <= 1.0:
                    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

            # Format Equity Panel
            if 'Equity' in ylabel and equity_series is not None:
                # Fill equity area
                x_vals = np.arange(len(plot_df))
                min_eq = equity_series.min()
                ax.fill_between(x_vals, equity_series.values, min_eq, color=equity_color, alpha=0.1)

            # Soft spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_linewidth(1.5)
            ax.spines['bottom'].set_linewidth(1.5)

        plt.subplots_adjust(top=0.92)
        
        cls._inject_logo(fig, kwargs)
        
        if savefig_kwargs:
            if isinstance(savefig_kwargs, dict):
                plt.savefig(**savefig_kwargs)
            else:
                plt.savefig(savefig_kwargs)
                
        if show_kwargs and plt.get_backend().lower() != 'agg':
            plt.show()
            
        return fig, axes
