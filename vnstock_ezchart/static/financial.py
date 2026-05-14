import os
import warnings
from typing import Union, List, Optional, Tuple, Dict, Any
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from ..config import *
from ..utils import Utils
import matplotlib.ticker as mticker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOGO_PATH = os.path.join(BASE_DIR, 'assets', 'vnstock_logo.png')
import pandas as pd
import random
from wordcloud import WordCloud
import seaborn as sns
import mplfinance as mpf
import numpy as np

class FinancialMixin:
        @classmethod
        def candle(cls, data: 'pd.DataFrame', title: str = '', figsize: Tuple[float, float] = (12, 8), volume: bool = True, overlays: list = None, subplots: list = None, **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            """
            Draws a candlestick chart combining volume data.
            Input data must be a pandas DataFrame with a Datetime index containing 'Open', 'High', 'Low', 'Close' columns. The 'Volume' column is optional.

            Args:
                data (pd.DataFrame): Stock price data.
                title (str): The title of the chart.
                figsize (tuple): The size of the chart.
                volume (bool): Displays trading volume. Defaults to True.
                color_palette (str): The color palette to use. Defaults to 'vnstock'.
                **kwargs: Additional keyword arguments for styling.
            """
            import mplfinance as mpf
        
            mpl_plot_instance = cls()
            palette_name = kwargs.pop('color_palette', cls._global_theme)
            palette = Utils.brand_palettes.get(palette_name, Utils.brand_palettes['vnstock'])
        
            # Soft Premium Colors (Use green/red from the palette if available, otherwise use default colors)
            up_color = palette[0] if len(palette) > 0 else '#4CAF50'
            down_color = palette[3] if len(palette) > 3 else '#EF5350'
            grid_color = '#f1f5f9'
            bg_color = '#ffffff'
            text_color = '#475569'

            mc = mpf.make_marketcolors(
                up=up_color,
                down=down_color,
                edge='inherit',
                wick='inherit',
                volume='in',
                ohlc='inherit'
            )
        
            s = mpf.make_mpf_style(
                marketcolors=mc,
                gridstyle='-',
                gridcolor=grid_color,
                facecolor=bg_color,
                edgecolor=bg_color,
                figcolor=bg_color,
                y_on_right=False,
                rc={
                    'patch.edgecolor': '#FFFFFF', 
                    'patch.force_edgecolor': True, 
                    'patch.linewidth': 1.0,
                    'axes.labelsize': 12,
                    'axes.labelcolor': text_color,
                    'xtick.color': text_color,
                    'ytick.color': text_color,
                    'axes.edgecolor': '#cbd5e1',
                }
            )
        
            # Ensure index is Datetime
            plot_df = data.copy()
            if not isinstance(plot_df.index, pd.DatetimeIndex):
                if 'time' in plot_df.columns:
                    plot_df = plot_df.set_index('time')
                elif 'date' in plot_df.columns:
                    plot_df = plot_df.set_index('date')
                plot_df.index = pd.to_datetime(plot_df.index)
            
            rename_map = {c: c.capitalize() for c in plot_df.columns if c.lower() in ['open', 'high', 'low', 'close', 'volume']}
            plot_df = plot_df.rename(columns=rename_map)

            font_name = kwargs.pop('font_name', plt.rcParams['font.family'])
            if isinstance(font_name, list):
                font_name = font_name[0]
            
            apds = []
            if overlays:
                for overlay in overlays:
                    if isinstance(overlay, dict):
                        apds.append(mpf.make_addplot(overlay['data'], type=overlay.get('type', 'line'), color=overlay.get('color', None), panel=0, alpha=overlay.get('alpha', 0.8), width=overlay.get('width', 1.0)))
                    else:
                        apds.append(mpf.make_addplot(overlay, type='line', panel=0, alpha=0.8, width=1.0))
                    
            if subplots:
                panel_idx = 2 if volume else 1
                for subplot in subplots:
                    if isinstance(subplot, dict):
                        apds.append(mpf.make_addplot(subplot['data'], type=subplot.get('type', 'line'), color=subplot.get('color', None), panel=panel_idx, secondary_y=subplot.get('secondary_y', False), ylabel=subplot.get('ylabel', ''), width=subplot.get('width', 1.0)))
                    else:
                        apds.append(mpf.make_addplot(subplot, type='line', panel=panel_idx, width=1.0))
                    panel_idx += 1
                
            # If we added subplots, we need to adjust panel_ratios
            panel_ratios = [4]
            if volume:
                panel_ratios.append(1)
            if subplots:
                for _ in subplots:
                    panel_ratios.append(1.5)
            
            mpf_kwargs = {
                'type': 'candle', 
                'volume': volume, 
                'style': s,
                'figsize': figsize,
                'title': "",
                'ylabel': 'Giá',
                'ylabel_lower': 'Khối lượng' if volume else '',
                'returnfig': True,
                'tight_layout': True,
                'xrotation': 0,
            }
            if apds:
                mpf_kwargs['addplot'] = apds
            if len(panel_ratios) > 1:
                mpf_kwargs['panel_ratios'] = panel_ratios
            
            mpf_kwargs.update(kwargs)

            fig, axes = mpf.plot(plot_df, **mpf_kwargs)
        
            # Customize font title
            if title:
                fig.suptitle(title, y=1.05, fontweight="black", fontname=font_name, fontsize=16, color='#111827')
        
            # Customize volume format và spines
            import matplotlib.ticker as mticker
            def format_volume(x, pos):
                if x >= 1e6:
                    return f'{x*1e-6:.1f}M'
                elif x >= 1e3:
                    return f'{x*1e-3:.0f}K'
                return f'{x:.0f}'
            
            for ax in axes:
                ylabel = ax.get_ylabel()
                if 'Khối lượng' in ylabel or 'Volume' in ylabel:
                    ax.set_ylabel('Khối lượng', fontsize=12, fontweight='medium', color=text_color, labelpad=10)
                    ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_volume))
                    if hasattr(ax.yaxis, 'offsetText'):
                        ax.yaxis.offsetText.set_visible(False)
                    for patch in ax.patches:
                        patch.set_edgecolor('#FFFFFF')
                        patch.set_linewidth(0.5)
                else:
                    ax.set_ylabel('Giá', fontsize=12, fontweight='medium', color=text_color, labelpad=10)
                    
                # Soft spines
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_linewidth(1.5)
                ax.spines['bottom'].set_linewidth(1.5)
            
            # Add extra padding for the title
            plt.subplots_adjust(top=0.92)
            plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, axes
        @classmethod
        def candlestick(cls, data, **kwargs):
            import warnings
            warnings.warn("'candlestick' is deprecated. Please use 'candle' instead.", DeprecationWarning, stacklevel=2)
            return cls.candle(data, **kwargs)
        @classmethod
        def equity_curve(cls, data: Union['pd.Series', 'pd.DataFrame'], benchmark: Optional[Union['pd.Series', 'pd.DataFrame']] = None, title: str = 'Equity Curve & Drawdown', figsize: Tuple[float, float] = (10, 6), **kwargs) -> Tuple['plt.Figure', 'plt.Axes', 'plt.Axes']:
            """
            Draws an equity curve (cumulative returns) with an underwater drawdown subplot.
        
            Args:
                data (pd.Series/pd.DataFrame): Cumulative returns series.
                benchmark (pd.Series): Optional benchmark cumulative returns.
                title (str): Chart title.
                figsize (tuple): Figure size.
            """
            import numpy as np
        
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
        
            palette_name = kwargs.pop('color_palette', cls._global_theme)
            palette = Utils.brand_palettes.get(palette_name, Utils.brand_palettes['vnstock'])
            main_color = palette[0] if len(palette) > 0 else '#4CAF50'
            bench_color = palette[1] if len(palette) > 1 else '#94a3b8'
        
            # Plot Equity Curve
            if isinstance(data, pd.DataFrame):
                data = data.iloc[:, 0]
            ax1.plot(data.index, data.values, color=main_color, linewidth=2, label='Strategy')
        
            if benchmark is not None:
                if isinstance(benchmark, pd.DataFrame):
                    benchmark = benchmark.iloc[:, 0]
                ax1.plot(benchmark.index, benchmark.values, color=bench_color, linewidth=1.5, linestyle='--', label='Benchmark')
            
            # Plot Drawdown
            running_max = data.cummax()
            drawdown = (data - running_max) / running_max
            ax2.fill_between(drawdown.index, drawdown.values, 0, color='#ef4444', alpha=0.3)
            ax2.plot(drawdown.index, drawdown.values, color='#ef4444', linewidth=1)
        
            style_kwargs = cls._filter_plot_kwargs(kwargs)
            cls.apply_chart_style(ax1, title=title, ylabel='Cumulative Return', show_xaxis=False, show_legend=True, **style_kwargs)
            cls.apply_chart_style(ax2, ylabel='Drawdown', ytick_format='{:.1%}', **style_kwargs)
        
            plt.tight_layout()
            cls._inject_logo(fig, kwargs)
            return fig, ax1, ax2
        @classmethod
        def returns_heatmap(cls, data: Union['pd.Series', 'pd.DataFrame'], title: str = 'Monthly Returns Heatmap', figsize: Tuple[float, float] = (10, 5), **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            """
            Draws a monthly returns heatmap (Year x Month matrix).
        
            Args:
                data (pd.Series/pd.DataFrame): Returns series (daily or monthly). If daily, it will be resampled to monthly.
            """
            import numpy as np
            import seaborn as sns
        
            if isinstance(data, pd.DataFrame):
                data = data.iloc[:, 0]
            
            # Ensure it is monthly. We check if the frequency is roughly daily
            if len(data) > 0 and (data.index[1] - data.index[0]).days < 20:
                try:
                    monthly_ret = data.resample('ME').apply(lambda x: (1 + x).prod() - 1)
                except ValueError:
                    monthly_ret = data.resample('M').apply(lambda x: (1 + x).prod() - 1)
            else:
                monthly_ret = data
            
            df_heatmap = pd.DataFrame({'Year': monthly_ret.index.year, 'Month': monthly_ret.index.month, 'Return': monthly_ret.values})
            pivot = df_heatmap.pivot(index='Year', columns='Month', values='Return')
        
            for m in range(1, 13):
                if m not in pivot.columns:
                    pivot[m] = np.nan
            pivot = pivot[range(1, 13)]
            pivot.columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
            cmap = sns.diverging_palette(10, 130, as_cmap=True)
            fig, ax = cls.heatmap(pivot, title=title, figsize=figsize, annot=True, fmt='.1%', cmap=cmap, center=0, 
                                  linewidths=1, linecolor='white', cbar_kws={'shrink': 0.8}, 
                                  annot_kws={"size": 8}, **kwargs)
        
            # Improve display interface for y and x axes
            if ax.get_yticklabels():
                ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
            ax.set_ylabel('')
            ax.set_xlabel('')
        
            cls._inject_logo(fig, kwargs)
            return fig, ax
