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

class StatisticalMixin:
        @classmethod
        def boxplot(cls, data: 'pd.DataFrame', **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            show_plot = kwargs.pop('show', True)
            """
            Represents data using a boxplot.

            Args:
                data (Union[pd.DataFrame, pd.Series]): Input data as a DataFrame or Series.
                title (str): The title of the chart.
                title_fontsize (int): The font size for the title.
                xlabel (str): The label for the X-axis.
                ylabel (str): The label for the Y-axis.
                color_palette (str): Name of a predefined color palette or a custom list of colors. Defaults to 'vnstock'. Available palettes: 'percentage', 'amount', 'category', 'trend', 'flatui', 'vnstock', 'learn_anything'.
                palette_shuffle (bool): Randomize the order of colors in the palette. Defaults to False.
                grid (bool): Displays the grid. True to show, False to hide.
                data_labels (bool): Displays data labels on the chart.
                data_label_format (str): The format for data labels. Accepts abbreviated values like '1K', '1M', '1B', '1T'.
                label_fontsize (int): The font size for the X and Y axis labels.
                legend_title (str): The title for the legend.
                show_legend (bool): Displays the legend. True to show, False to hide.
                legend_fontsize (int): The font size for the legend.
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
            mpl_plot_instance = cls()
            mpl_plot_instance.utils.apply_palette(kwargs.pop('color_palette', cls._global_theme), kwargs.pop('palette_shuffle', False))

            ax = kwargs.pop('ax', None)
            if ax is None:
                fig, ax = plt.subplots()
            else:
                fig = ax.figure
        
            style_kwargs = {k: kwargs.pop(k, None) for k in ['title', 'xlabel', 'ylabel', 'grid', 'legend_title', 'data_labels', 'data_label_format',
                                                            'series_names', 'font_name', 'show_legend', 'show_xaxis', 
                                                            'show_yaxis', 'title_fontsize', 'label_fontsize', 
                                                            'tick_labelsize', 'legend_fontsize', 'xtick_format', 
                                                            'ytick_format', 'figsize', 'xlim', 'ylim', 'tick_rotation', 
                                                            'background_color', 'bar_edge_color', 'grid_axis',
                                                            'data_label_position', 'data_label_color', 'data_label_fontsize']}

            plot_kwargs = cls._filter_plot_kwargs(kwargs)
            data.plot(kind='box', ax=ax, **plot_kwargs)
            cls.apply_chart_style(ax, **style_kwargs)
            if show_plot and plt.get_backend().lower() != 'agg':
                plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, ax
        @classmethod
        def pairplot(cls, data, **kwargs):
            """
            Represents data using a pairplot.

            Args:
                data (pd.DataFrame): Input data to represent.
                **kwargs: Custom parameters for the chart (supports Seaborn options).
            """
            g = sns.pairplot(data, **kwargs)
            cls._inject_logo(g.figure, kwargs)
            return g
