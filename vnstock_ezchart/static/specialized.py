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

class SpecializedMixin:
        @classmethod
        def treemap(cls, values, labels, title='', color_palette='vnstock', palette_shuffle=False, figsize=(10,8), title_fontsize=14, **kwargs):
            """
            Draws a treemap.

            Args:
                values (Union[list, pd.Series]): The data values to plot.
                labels (list): The labels for each section of the treemap.
                title (str): The title of the chart.
                color_palette (str): Name of a predefined color palette or a custom list of colors. Defaults to 'vnstock'. Available palettes: 'percentage', 'amount', 'category', 'trend', 'flatui', 'vnstock', 'learn_anything'.
                palette_shuffle (bool): Randomize the order of colors in the palette. Defaults to False.
                figsize (tuple): The size of the chart, e.g., (10, 6).
                title_fontsize (int): The font size for the title.
                fontsize (int): The font size for the text inside the treemap. Defaults to 10.
                color (str): The text color. Defaults to 'white'.
            """
            colors = Utils.brand_palettes[color_palette]

            if palette_shuffle:
                random.shuffle(colors)

            fig, ax = plt.subplots(figsize=figsize) 
            squarify.plot(sizes=values, label=labels, pad=0.2,
                        text_kwargs={'fontsize': 10, 'color': 'white', 'fontweight': 'bold'},
                        color=colors, ax=ax, edgecolor='white', linewidth=2)
            fig.suptitle(title, y=0.98, fontweight="black", fontname=kwargs.get('font_name'), fontsize=title_fontsize or 16, color='#111827')
            ax.axis('off')
            cls._inject_logo(fig, kwargs)
            return fig, ax
        @classmethod
        def heatmap(cls, data: 'pd.DataFrame', **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            """
            Represents data as a heatmap.

            Args:
                data (pd.DataFrame): Input data as a DataFrame.
                title (str): The title of the chart.
                font_name (str): The name of the font to apply.
                figsize (tuple): The size of the chart, e.g., (10, 6).
                xlim (tuple): The limits for the X-axis, e.g., (0, 100).
                ylim (tuple): The limits for the Y-axis, e.g., (0, 100).
                title_fontsize (int): The font size for the title.
                background_color (str): The background color for the chart.
            """
            figsize = kwargs.get('figsize', (10, 6))
            fig, ax = plt.subplots(figsize=figsize)
            mpl_plot_instance = cls()
            mpl_plot_instance.utils.apply_palette(kwargs.pop('color_palette', cls._global_theme), kwargs.pop('palette_shuffle', False))
        
            # Note: For heatmaps, not all styling arguments apply (e.g., data_labels)
            style_kwargs = {k: kwargs.pop(k, None) for k in ['title', 'font_name', 'figsize', 'xlim', 'ylim', 
                                                            'title_fontsize', 'background_color']}

            plot_kwargs = cls._filter_plot_kwargs(kwargs)
            sns.heatmap(data, ax=ax, **plot_kwargs)
            cls.apply_chart_style(ax, **style_kwargs)
        
            # Remove tick marks that intrude into heatmap cells causing "crosshairs"
            ax.tick_params(length=0)
            ax.grid(False)
        
            plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, ax
        @classmethod
        def wordcloud(cls, text, title="Word Cloud", color_palette='vnstock', palette_shuffle=False,
                        max_words=100, width=800, height=400, figsize=(10, 8),
                        fontname=None, savefig=None, show=True):
            """"
            Represents data as a word cloud.

            Args:
                text (str): Input data as text.
                title (str): The title of the chart.
                color_palette (str): Name of a predefined color palette or a custom list of colors. Defaults to 'vnstock'. Available palettes: 'percentage', 'amount', 'category', 'trend', 'flatui', 'vnstock', 'learn_anything'.
                palette_shuffle (bool): Randomize the order of colors in the palette. Defaults to False.
                max_words (int): Maximum number of words to display.
                width (int): The width of the chart.
                height (int): The height of the chart.
                figsize (tuple): The size of the chart, e.g., (10, 6).
                fontname (str): The name of the font to apply.
                savefig (str): Path to save the image file. Defaults to None.
                show (bool): Displays the chart. Defaults to True.
            """
        
            colors = Utils.brand_palettes[color_palette]

            if palette_shuffle:
                random.shuffle(colors)

            custom_cmap = Utils.create_cmap(colors)

            # Generate word cloud
            wordcloud = WordCloud(width=width, height=height, background_color="white", colormap=custom_cmap, max_words=max_words).generate(text)

            # Create plot
            fig, ax = plt.subplots(figsize=figsize)
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")

            fig.suptitle(title, y=0.98, fontweight="bold", fontname=fontname, fontsize=14, color="black")

            fig.set_facecolor("white")
            ax.set_facecolor("white")

            try:
                plt.subplots_adjust(hspace=0, bottom=0, top=0.9)
            except Exception:
                pass

            cls._inject_logo(fig, {})

            if savefig:
                if isinstance(savefig, dict):
                    plt.savefig(**savefig)
                else:
                    plt.savefig(savefig)
            if show:
                plt.show()
            
            return fig, ax
        @classmethod
        def table(
            cls,
            data,
            columns=None,
            title="",
            title_loc="left",
            header=True,
            colWidths=None,
            rowLoc="right",
            colLoc="right",
            colLabels=None,
            edges="horizontal",
            orient="horizontal",
            figsize=(5.5, 6),
            savefig=None,
            show=False
        ):
        
            """
                Plots a table using matplotlib.

                Args:
                    data (pd.DataFrame): Data to plot.
                    columns (list, optional): Columns to display. Defaults to None.
                    title (str, optional): The title of the table. Defaults to "".
                    title_loc (str, optional): Title location. Defaults to "left".
                    header (bool, optional): Whether to display the header row. Defaults to True.
                    colWidths (list, optional): Widths of the columns. Defaults to None.
                    rowLoc (str, optional): Data alignment for rows. Defaults to "right".
                    colLoc (str, optional): Data alignment for columns. Defaults to "right".
                    colLabels (list, optional): Column titles. Defaults to None.
                    edges (str, optional): Borders of the table. Defaults to "horizontal".
                    orient (str, optional): Orientation of the table. Defaults to "horizontal".
                    figsize (tuple, optional): The size of the table. Defaults to (5.5, 6).
                    savefig (str, optional): Path to save the file. Defaults to None.
                    show (bool, optional): Displays the table. Defaults to False.
            """

            if columns is not None:
                try:
                    data.columns = columns
                except Exception:
                    pass

            fig = plt.figure(figsize=figsize)
            ax = plt.subplot(111, frame_on=False)

            if title != "":
                ax.set_title(
                    title, fontweight="bold", fontsize=14, color="black", loc=title_loc
                )

            the_table = ax.table(
                cellText=data.values,
                colWidths=colWidths,
                rowLoc=rowLoc,
                colLoc=colLoc,
                edges=edges,
                colLabels=(data.columns if header else colLabels),
                loc="center",
                zorder=2,
            )

            the_table.auto_set_font_size(False)
            the_table.set_fontsize(12)
            the_table.scale(1, 1)

            for (row, col), cell in the_table.get_celld().items():
                cell.set_height(0.08)
                cell.set_text_props(color="#475569")
                cell.set_edgecolor("#f1f5f9") # Very light gray for internal borders
            
                if row == 0 and header:
                    # Header styling
                    cell.set_edgecolor("#66BB6A") # Vnstock Soft Green for header border
                    cell.set_facecolor("#E8F5E9") # Very light green background
                    cell.set_linewidth(1.5)
                    cell.set_text_props(weight="bold", color="#1B5E20")
                elif col == -1: # Row labels if any
                    cell.set_linewidth(0)
                elif row > 0:
                    # Alternating row colors for better readability (zebra striping)
                    if row % 2 == 0:
                        cell.set_facecolor("#F8FAFC")
                    else:
                        cell.set_facecolor("#FFFFFF")
                    cell.set_linewidth(1)

            ax.grid(False)
            ax.set_xticks([])
            ax.set_yticks([])

            try:
                plt.subplots_adjust(hspace=0)
            except Exception:
                pass
            try:
                fig.tight_layout(w_pad=0, h_pad=0)
            except Exception:
                pass

            if savefig:
                if isinstance(savefig, dict):
                    plt.savefig(**savefig)
                else:
                    plt.savefig(savefig)

            if show:
                plt.show(block=False)

            plt.close()

            if not show:
                cls._inject_logo(fig, {})
            return fig

            return None

        @classmethod
        def summary_card(cls, ticker: str, company_name: str, current_price: float, price_change: float, price_change_pct: float,
                         metrics: dict, sparkline_data: pd.Series, signal: str, **kwargs):
            """
            Draws a Stock Summary Card.
            
            Args:
                ticker (str): Stock ticker symbol.
                company_name (str): Full name of the company.
                current_price (float): Current stock price.
                price_change (float): Absolute price change.
                price_change_pct (float): Percentage price change.
                metrics (dict): Dictionary of fundamental/technical metrics. Max 6 items recommended.
                sparkline_data (pd.Series): Data for the miniature trend chart (last 30 days).
                signal (str): Technical signal (e.g., 'Tích cực', 'Tiêu cực', 'Trung tính').
            """
            from matplotlib.patches import FancyBboxPatch
            import matplotlib.patheffects as path_effects
            
            figsize = kwargs.get('figsize', (9, 5))
            fig = plt.figure(figsize=figsize, facecolor='#f8fafc')
            
            # Create a main axis that fills the figure for placing text and patches
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis('off')
            
            # Draw main card background
            card = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.02,rounding_size=0.03", 
                                  ec='#e2e8f0', fc='#ffffff', lw=1.5)
            # Add a subtle shadow
            card.set_path_effects([path_effects.SimplePatchShadow(offset=(0, -2), alpha=0.05), path_effects.Normal()])
            ax.add_patch(card)
            
            # --- HEADER ---
            # Ticker
            ax.text(0.06, 0.88, ticker, fontsize=32, fontweight='black', color='#0f172a', fontname=kwargs.get('font_name', 'Inter'), va='center')
            
            # Company Name
            max_len = 45
            company_disp = company_name[:max_len] + '...' if len(company_name) > max_len else company_name
            ax.text(0.06, 0.80, company_disp, fontsize=12, color='#64748b', fontname=kwargs.get('font_name', 'Inter'), va='center')
            
            # Price
            ax.text(0.94, 0.88, f"{current_price:,.0f} ₫", fontsize=28, fontweight='bold', color='#0f172a', fontname=kwargs.get('font_name', 'Inter'), ha='right', va='center')
            
            # Price Change
            is_positive = price_change >= 0
            change_color = '#10b981' if is_positive else '#ef4444'
            change_sign = '+' if is_positive else ''
            arrow = '▲' if is_positive else '▼'
            change_text = f"{arrow} {change_sign}{price_change:,.0f} ({change_sign}{price_change_pct:.2f}%)"
            ax.text(0.94, 0.80, change_text, fontsize=14, fontweight='bold', color=change_color, fontname=kwargs.get('font_name', 'Inter'), ha='right', va='center')
            
            # --- SIGNAL & SPARKLINE LABELS ---
            lang = kwargs.get('lang', cls._global_lang)
            labels = {
                'vi': {'recommendation': 'Đánh giá', 'trend': 'Xu hướng 30 ngày'},
                'en': {'recommendation': 'Rating', 'trend': '30-day Trend'}
            }
            l = labels.get(lang, labels['vi'])
            
            # Signal Ribbon
            signal_color_map = {'Tích cực': '#10b981', 'Tiêu cực': '#ef4444', 'Trung tính': '#f59e0b',
                                'Positive': '#10b981', 'Negative': '#ef4444', 'Neutral': '#f59e0b'}
            s_color = signal_color_map.get(signal, '#64748b')
            s_bg = s_color + '1A' # 10% opacity
            
            # Auto-translate signal if needed
            signals = {
                'vi': {'Tích cực': 'TÍCH CỰC', 'Tiêu cực': 'TIÊU CỰC', 'Trung tính': 'TRUNG TÍNH', 'Positive': 'TÍCH CỰC', 'Negative': 'TIÊU CỰC', 'Neutral': 'TRUNG TÍNH'},
                'en': {'Tích cực': 'POSITIVE', 'Tiêu cực': 'NEGATIVE', 'Trung tính': 'NEUTRAL', 'Positive': 'POSITIVE', 'Negative': 'NEGATIVE', 'Neutral': 'NEUTRAL'}
            }
            s_map = signals.get(lang, signals['vi'])
            signal_text = s_map.get(signal, signal.upper())

            signal_box = FancyBboxPatch((0.06, 0.63), 0.22, 0.08, boxstyle="round,pad=0.01,rounding_size=0.02", 
                                        ec='none', fc=s_bg)
            ax.add_patch(signal_box)
            ax.text(0.17, 0.69, l['recommendation'], fontsize=10, color=s_color, ha='center', va='center', fontweight='medium', fontname=kwargs.get('font_name', 'Inter'))
            ax.text(0.17, 0.65, signal_text, fontsize=14, color=s_color, ha='center', va='center', fontweight='black', fontname=kwargs.get('font_name', 'Inter'))

            # --- SPARKLINE ---
            # Create a small axes for the sparkline
            ax_spark = fig.add_axes([0.65, 0.62, 0.29, 0.12])
            ax_spark.axis('off')
            ax_spark.plot(sparkline_data.values, color=change_color, lw=2)
            # Add subtle fill
            ax_spark.fill_between(range(len(sparkline_data)), sparkline_data.values, sparkline_data.min(), 
                                  color=change_color, alpha=0.1)
            ax_spark.set_ylim(sparkline_data.min() - (sparkline_data.max()-sparkline_data.min())*0.1, 
                              sparkline_data.max() + (sparkline_data.max()-sparkline_data.min())*0.1)
            ax.text(0.94, 0.58, l['trend'], fontsize=10, color='#64748b', fontname=kwargs.get('font_name', 'Inter'), ha='right', va='center')

            # --- METRICS GRID ---
            # Draw a subtle separator
            ax.plot([0.06, 0.94], [0.52, 0.52], color='#f1f5f9', lw=1.5)
            
            # Position metrics in a 2x3 grid
            xs = [0.06, 0.40, 0.72]
            ys = [0.35, 0.15]
            
            for i, (key, val) in enumerate(metrics.items()):
                if i >= 6: break
                x = xs[i % 3]
                y = ys[i // 3]
                # Label
                ax.text(x, y + 0.07, key, fontsize=11, color='#64748b', fontname=kwargs.get('font_name', 'Inter'), fontweight='medium')
                # Value
                ax.text(x, y, str(val), fontsize=18, fontweight='bold', color='#0f172a', fontname=kwargs.get('font_name', 'Inter'))

            kwargs['logo_position'] = (0.80, 0.06, 0.12, 0.06)
            cls._inject_logo(fig, kwargs, force_right=True)
            return fig, ax
