import os
import warnings
from typing import Union, List, Optional, Tuple, Dict, Any
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from ..config import *
from ..utils import Utils
import matplotlib.ticker as mticker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOGO_PATH = os.path.join(BASE_DIR, 'assets', 'vnstock_logo.png')
import pandas as pd
import random
from wordcloud import WordCloud
import seaborn as sns
import mplfinance as mpf
import numpy as np

class StyleMixin:
        _global_theme = 'vnstock'
        _global_logo_path = DEFAULT_LOGO_PATH
        _global_font = None
        _global_lang = 'vi'
        _NON_PLOT_KWARGS = {'show', 'savefig', 'logo_position', 'lang'}

        @staticmethod
        def _filter_plot_kwargs(kwargs):
            """Remove non-plotting kwargs that should not be forwarded to pandas/seaborn/mplfinance."""
            return {k: v for k, v in kwargs.items() if k not in StyleMixin._NON_PLOT_KWARGS}

        @classmethod
        def set_theme(cls, theme_name: str = 'vnstock', logo_path: Optional[str] = DEFAULT_LOGO_PATH, font_name: Optional[str] = None, lang: str = 'vi'):
            """
            Sets the global theme configuration for all charts.
        
            Args:
                theme_name (str): Name of the color palette (e.g., 'vnstock', 'flatui').
                logo_path (str): Path or URL to the logo image. Set to None to disable.
                font_name (str): Name of the font to apply globally.
                lang (str): Global language for labels ('vi' or 'en'). Defaults to 'vi'.
            """
            cls._global_theme = theme_name
            cls._global_logo_path = logo_path
            cls._global_lang = lang
        
            # Embedding the default Inter font if available
            import os
            from matplotlib import font_manager
        
            inter_path = os.path.join(BASE_DIR, 'assets', 'fonts', 'Inter-Regular.ttf')
            if os.path.exists(inter_path):
                try:
                    font_manager.fontManager.addfont(inter_path)
                    if not font_name:
                        font_name = 'Inter'
                except Exception:
                    pass

            cls._global_font = font_name
            if font_name:
                plt.rcParams['font.family'] = font_name
        @staticmethod
        def apply_chart_style(ax, 
                            title=None, title_fontsize=14, 
                            xlabel=None, ylabel=None, grid=None, 
                            data_labels=None, data_label_format='1K', label_fontsize=None, 
                            legend_title=None, show_legend=True, legend_fontsize=None, 
                            series_names=None, 
                            font_name=None, figsize=None, 
                            show_xaxis=True, show_yaxis=True, 
                            tick_labelsize=None, xtick_format=None, 
                            ytick_format=None, tick_rotation=None, 
                            xlim=None, ylim=None, 
                            background_color=None, bar_edge_color=None, grid_axis='both', 
                            data_label_position='outside', data_label_color='#475569', data_label_fontsize=10, **kwargs):
            """
            Applies style customizations to the chart.

            Args:
                ax (matplotlib.axes.Axes): The chart axis.
                title (str): The title of the chart.
                title_fontsize (int): The font size for the title.
                xlabel (str): The label for the X-axis.
                ylabel (str): The label for the Y-axis.
                grid (bool): Displays the grid. True to show, False to hide.
                data_labels (bool): Displays data labels on the chart.
                data_label_format (str): The format for data labels. Accepts abbreviated values like '1K', '1M', '1B', '1T'.
                label_fontsize (int): The font size for the X and Y axis labels.
                legend_title (str): The title for the legend.
                show_legend (bool): Displays the legend. True to show, False to hide.
                series_names (list): A list of names for the data series in the chart.
                font_name (str): The name of the font to apply.
                figsize (tuple): The size of the chart, e.g., (10, 6).
                show_xaxis (bool): Displays the X-axis. True to show, False to hide.
                show_yaxis (bool): Displays the Y-axis. True to show, False to hide.
                tick_labelsize (int): The font size for the axis tick labels.
                xtick_format (str): The format for the X-axis tick labels. For example, decimal format '{:.0f}'.
                ytick_format (str): The format for the Y-axis tick labels. For example, percentage format '{:.0%}'.
                tick_rotation (int): The rotation angle for the axis tick labels.
                xlim (tuple): The limits for the X-axis, e.g., (0, 100).
                ylim (tuple): The limits for the Y-axis, e.g., (0, 100).
                background_color (str): The background color for the chart.
                bar_edge_color (str): The edge color for the bars in the chart.
            """
            if font_name:
                plt.rcParams['font.family'] = font_name
            if title:
                ax.set_title(title, fontsize=title_fontsize or 16, fontweight='black', color='#111827', pad=16)
            if xlabel:
                ax.set_xlabel(xlabel, fontsize=label_fontsize or 12, fontweight='medium', color='#475569', labelpad=10)
            if ylabel:
                ax.set_ylabel(ylabel, fontsize=label_fontsize or 12, fontweight='medium', color='#475569', labelpad=10)
        
            if grid:
                ax.grid(True, axis=grid_axis or 'both', color='#f1f5f9', linestyle='-', linewidth=1.5, alpha=0.7)
                ax.set_axisbelow(True)

            # Soft Spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cbd5e1')
            ax.spines['bottom'].set_color('#cbd5e1')
            ax.spines['left'].set_linewidth(1.5)
            ax.spines['bottom'].set_linewidth(1.5)

            # Tick params
            ax.tick_params(axis='both', which='major', labelsize=tick_labelsize or 10, colors='#64748b', width=1.5, length=5)
            ax.tick_params(axis='both', which='minor', colors='#64748b')

            if data_labels:
                formatter = mticker.FuncFormatter(lambda x, pos: Utils.readable_format(x, data_label_format))
                for p in ax.patches:
                    h = p.get_height()
                    if h == 0: continue
                    if data_label_position == 'center':
                        y_pos = p.get_y() + h / 2.0
                        va = 'center'
                        xytext = (0, 0)
                    else:
                        y_pos = p.get_y() + h
                        va = 'bottom' if h > 0 else 'top'
                        xytext = (0, 5 if h > 0 else -5)
                    ax.annotate(formatter(h), 
                                (p.get_x() + p.get_width() / 2., y_pos), 
                                ha='center', va=va, xytext=xytext, textcoords='offset points',
                                color=data_label_color, fontweight='medium', fontsize=data_label_fontsize)
                
            if show_legend:
                has_labels = any(l.get_label() for l in ax.get_lines() + ax.patches if not l.get_label().startswith('_'))
                if series_names or legend_title or has_labels:
                    legend = ax.legend(title=legend_title, labels=series_names, fontsize=legend_fontsize) if series_names else ax.legend(title=legend_title, fontsize=legend_fontsize)
                    if legend.get_title():
                        legend.get_title().set_fontweight('bold')
                        legend.get_title().set_color('#111827')
                    for text in legend.get_texts():
                        text.set_color('#475569')
                    legend.get_frame().set_linewidth(0.0)
                    legend.get_frame().set_facecolor('#ffffff')
                    legend.get_frame().set_alpha(0.8)
            else:
                ax.legend().set_visible(False)
            
            if figsize:
                ax.figure.set_size_inches(figsize)
            if xlim:
                ax.set_xlim(xlim)
            if ylim:
                ax.set_ylim(ylim)
            if tick_rotation:
                plt.xticks(rotation=tick_rotation)
            
            if background_color:
                ax.set_facecolor(background_color)
                ax.figure.set_facecolor(background_color)
            else:
                # Default soft background
                ax.set_facecolor('#ffffff')
                ax.figure.set_facecolor('#ffffff')
            
            if xtick_format:
                formatter = mticker.FuncFormatter(
                    lambda x, _: xtick_format.format(x)
                )
                ax.xaxis.set_major_formatter(formatter)
            if ytick_format:
                formatter = mticker.FuncFormatter(
                    lambda y, _: ytick_format.format(y)
                )
                ax.yaxis.set_major_formatter(formatter)
            
            if bar_edge_color:
                for p in ax.patches:
                    p.set_edgecolor(bar_edge_color)
                    p.set_linewidth(1.5)
            else:
                # Add subtle edge to bars by default for a soft look
                for p in ax.patches:
                    p.set_edgecolor('#ffffff')
                    p.set_linewidth(1.0)
                
            if show_xaxis is False:
                ax.xaxis.set_visible(False)
            if show_yaxis is False:
                ax.yaxis.set_visible(False)
                ax.spines['left'].set_visible(False)
        @classmethod
        def _inject_logo(cls, fig, kwargs, force_right=False):
            if not getattr(cls, '_global_logo_path', None):
                return
            
            has_xlabel = force_right or any(bool(a.get_xlabel()) for a in fig.axes if hasattr(a, 'get_xlabel'))
            default_pos = (0.80, 0.02, 0.12, 0.06) if has_xlabel else (0.44, 0.02, 0.12, 0.06)
        
            pos = kwargs.get('logo_position', default_pos)
            cls.add_logo(fig, logo_path=cls._global_logo_path, position=pos)
        @staticmethod
        def add_logo(fig, logo_path: str = DEFAULT_LOGO_PATH, position: Tuple[float, float, float, float] = (0.44, 0.02, 0.12, 0.06), adjust_bottom: float = 0.18) -> None:
            """
            Safely adds a logo to the figure canvas.
        
            Args:
                fig (matplotlib.figure.Figure): The figure object.
                logo_path (str): Path to the logo image.
                position (Tuple[float, float, float, float]): Bounding box (left, bottom, width, height) in figure fraction. Defaults to bottom center.
                adjust_bottom (float): Bottom margin to avoid overlapping with chart.
            """
            import matplotlib.image as mpimg
            import requests
            from io import BytesIO

            try:
                # Adjust the bottom margin of the figure to prevent the logo from overlapping with the data
                if adjust_bottom:
                    fig.subplots_adjust(bottom=adjust_bottom)

                # Check if it's a URL or local path
                if isinstance(logo_path, str) and logo_path.startswith('http'):
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(logo_path, headers=headers, timeout=10)
                    if response.status_code == 200:
                        img = mpimg.imread(BytesIO(response.content), format='png')
                    else:
                        print(f"Error: Could not download logo from {logo_path}. Status code: {response.status_code}")
                        return
                else:
                    img = mpimg.imread(logo_path)
                
                # Create a separate axes specifically for the logo to avoid overlap
                ax_logo = fig.add_axes(position, zorder=999)
                ax_logo.imshow(img)
                ax_logo.axis('off')
            except Exception as e:
                print(f"Error adding logo: {e}")
        def help(self, method_path):
            """
            Displays detailed information about a method based on its path.

            Args:
                method_path (str): The path to the method to retrieve detailed information for (e.g., 'bar' or 'Chart.bar').
            """
            parts = method_path.split('.')
            obj = self
            for part in parts[:-1]:
                try:
                    obj = getattr(obj, part)
                except AttributeError:
                    print(f"Attribute '{part}' not found.")
                    return
        
            method_name = parts[-1]
            try:
                method = getattr(obj, method_name)
                print(method.__doc__)
            except AttributeError:
                print(f"Method or property '{method_name}' not found in '{obj.__class__.__name__}'.")
