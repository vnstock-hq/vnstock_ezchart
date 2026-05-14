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

class BasicMixin:
        @classmethod
        def bar(cls, data: Union['pd.DataFrame', 'pd.Series'], **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            """
            Draws a bar chart.

            Args:
                data (Union[pd.DataFrame, pd.Series]): Input data as a DataFrame or Series.
                title (str): Chart title.
                title_fontsize (int): Font size for the title.
                xlabel (str): X-axis label.
                ylabel (str): Y-axis label.
                color_palette (Union[str, List[str]]): Palette name or list of colors. Defaults to global theme.
                palette_shuffle (bool): Randomize colors in palette. Default is False.
                grid (bool): Show grid lines.
                data_labels (bool): Display value labels on bars/points.
                data_label_format (str): Format string for labels (e.g., '1K', '1M').
                label_fontsize (int): Axis label font size.
                legend_title (str): Legend title.
                show_legend (bool): Show legend. Default is True.
                series_names (List[str]): Custom names for data series.
                font_name (str): Custom font family.
                figsize (Tuple[float, float]): Figure size (width, height).
                show_xaxis (bool): Show X-axis ticks.
                show_yaxis (bool): Show Y-axis ticks.
                tick_labelsize (int): Tick label font size.
                xtick_format (str): X-axis tick format (e.g., '{:.0f}').
                ytick_format (str): Y-axis tick format (e.g., '{:.0%}').
                tick_rotation (int): Rotation angle for ticks.
                xlim (Tuple[float, float]): X-axis limits.
                ylim (Tuple[float, float]): Y-axis limits.
                background_color (str): Background hex color.
                bar_edge_color (str): Bar edge hex color.
            """
            mpl_plot_instance = cls()
            mpl_plot_instance.utils.apply_palette(kwargs.pop('color_palette', cls._global_theme), kwargs.pop('palette_shuffle', False))
        
            style_kwargs = {k: kwargs.pop(k, None) for k in ['title', 'xlabel', 'ylabel', 'grid', 'data_labels', 'data_label_format',
                                                            'legend_title', 'series_names', 'font_name', 
                                                            'show_legend', 'show_xaxis', 'show_yaxis', 
                                                            'title_fontsize', 'label_fontsize', 'tick_labelsize', 
                                                            'legend_fontsize', 'xtick_format', 'ytick_format', 
                                                            'figsize', 'xlim', 'ylim', 'tick_rotation', 
                                                            'background_color', 'grid_color', 'grid_linestyle', 
                                                            'bar_edge_color', 'grid_axis', 'data_label_position', 
                                                            'data_label_color', 'data_label_fontsize']}
        
            ax = kwargs.pop('ax', None)
            if ax is None:
                fig, ax = plt.subplots()
            plot_kwargs = cls._filter_plot_kwargs(kwargs)
            data.plot(kind='bar', ax=ax, **plot_kwargs)
            cls.apply_chart_style(ax, **style_kwargs)
            plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, ax
        @classmethod
        def hist(cls, data: Union['pd.DataFrame', 'pd.Series'], **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            """
            Represents the data distribution using a histogram.
        
            Args:
                data (Union[pd.DataFrame, pd.Series]): Input data as a DataFrame or Series.
                title (str): Chart title.
                title_fontsize (int): Font size for the title.
                xlabel (str): X-axis label.
                ylabel (str): Y-axis label.
                color_palette (Union[str, List[str]]): Palette name or list of colors. Defaults to global theme.
                palette_shuffle (bool): Randomize colors in palette. Default is False.
                grid (bool): Show grid lines.
                data_labels (bool): Display value labels on bars/points.
                data_label_format (str): Format string for labels (e.g., '1K', '1M').
                label_fontsize (int): Axis label font size.
                legend_title (str): Legend title.
                show_legend (bool): Show legend. Default is True.
                series_names (List[str]): Custom names for data series.
                font_name (str): Custom font family.
                figsize (Tuple[float, float]): Figure size (width, height).
                show_xaxis (bool): Show X-axis ticks.
                show_yaxis (bool): Show Y-axis ticks.
                tick_labelsize (int): Tick label font size.
                xtick_format (str): X-axis tick format (e.g., '{:.0f}').
                ytick_format (str): Y-axis tick format (e.g., '{:.0%}').
                tick_rotation (int): Rotation angle for ticks.
                xlim (Tuple[float, float]): X-axis limits.
                ylim (Tuple[float, float]): Y-axis limits.
                background_color (str): Background hex color.
                bar_edge_color (str): Bar edge hex color.
            """
            mpl_plot_instance = cls()
            mpl_plot_instance.utils.apply_palette(kwargs.pop('color_palette', cls._global_theme), kwargs.pop('palette_shuffle', False))

            ax = kwargs.pop('ax', None)
            if ax is None:
                fig, ax = plt.subplots()
            else:
                fig = ax.figure
        
            style_kwargs = {k: kwargs.pop(k, None) for k in ['title', 'xlabel', 'ylabel', 'grid', 'data_labels', 'data_label_format',
                                                            'legend_title', 'series_names', 'font_name', 
                                                            'show_legend', 'show_xaxis', 'show_yaxis', 
                                                            'title_fontsize', 'label_fontsize', 'tick_labelsize', 
                                                            'legend_fontsize', 'xtick_format', 'ytick_format', 
                                                            'figsize', 'xlim', 'ylim', 'tick_rotation', 
                                                            'background_color', 'bar_edge_color', 'grid_axis',
                                                            'data_label_position', 'data_label_color', 'data_label_fontsize']}

            plot_kwargs = cls._filter_plot_kwargs(kwargs)
            data.plot(kind='hist', ax=ax, **plot_kwargs)
            cls.apply_chart_style(ax, **style_kwargs)
            plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, ax
        @classmethod
        def pie(cls, data: Union[list, 'pd.Series'], labels: list, **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            """
            Represents data as a pie chart.

            Args:
                data (Union[list, pd.Series]): Input data as a list or Series.
                labels (list): Labels for each slice of the pie chart.
                title (str): The title of the chart.
                color_palette (str): Name of a predefined color palette or a custom list of colors. Defaults to 'vnstock'. Available palettes: 'percentage', 'amount', 'category', 'trend', 'flatui', 'vnstock', 'learn_anything'. List all palettes with Utils.brand_palettes.keys().
                palette_shuffle (bool): Randomize the order of colors in the palette. Defaults to False.
                legend_title (str): The title for the legend.
                series_names (list): A list of names for the data series in the chart.
                figsize (tuple): The size of the chart, e.g., (10, 6).
                font_name (str): The name of the font to apply.
                show_legend (bool): Displays the legend. True to show, False to hide.
                title_fontsize (int): The font size for the title.
                legend_fontsize (int): The font size for the legend.
            """
            fig, ax = plt.subplots()
            mpl_plot_instance = cls()
            mpl_plot_instance.utils.apply_palette(kwargs.pop('color_palette', cls._global_theme), kwargs.pop('palette_shuffle', False))
        
            style_kwargs = {k: kwargs.pop(k, None) for k in ['title', 'legend_title', 'series_names', 'font_name', 
                                                            'show_legend', 'title_fontsize', 'legend_fontsize', 
                                                            'figsize']}

            if 'wedgeprops' not in kwargs:
                kwargs['wedgeprops'] = {'edgecolor': 'white', 'linewidth': 2, 'antialiased': True}
            if 'textprops' not in kwargs:
                kwargs['textprops'] = {'color': '#111827', 'fontweight': 'medium'}

            plot_kwargs = cls._filter_plot_kwargs(kwargs)
            data.plot(kind='pie', labels=labels, ax=ax, autopct='%1.1f%%', **plot_kwargs)
            cls.apply_chart_style(ax, **style_kwargs)
            plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, ax
        @classmethod
        def line(cls, data: Union['pd.DataFrame', 'pd.Series'], **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            """
            Represents data over time (timeseries). Data must have a datetime index.

            Args:
                data (Union[pd.DataFrame, pd.Series]): Input data as a DataFrame or Series.
                title (str): Chart title.
                title_fontsize (int): Font size for the title.
                xlabel (str): X-axis label.
                ylabel (str): Y-axis label.
                color_palette (Union[str, List[str]]): Palette name or list of colors. Defaults to global theme.
                palette_shuffle (bool): Randomize colors in palette. Default is False.
                grid (bool): Show grid lines.
                data_labels (bool): Display value labels on bars/points.
                data_label_format (str): Format string for labels (e.g., '1K', '1M').
                label_fontsize (int): Axis label font size.
                legend_title (str): Legend title.
                show_legend (bool): Show legend. Default is True.
                series_names (List[str]): Custom names for data series.
                font_name (str): Custom font family.
                figsize (Tuple[float, float]): Figure size (width, height).
                show_xaxis (bool): Show X-axis ticks.
                show_yaxis (bool): Show Y-axis ticks.
                tick_labelsize (int): Tick label font size.
                xtick_format (str): X-axis tick format (e.g., '{:.0f}').
                ytick_format (str): Y-axis tick format (e.g., '{:.0%}').
                tick_rotation (int): Rotation angle for ticks.
                xlim (Tuple[float, float]): X-axis limits.
                ylim (Tuple[float, float]): Y-axis limits.
                background_color (str): Background hex color.
                bar_edge_color (str): Bar edge hex color.
            """
            mpl_plot_instance = cls()
            mpl_plot_instance.utils.apply_palette(kwargs.pop('color_palette', cls._global_theme), kwargs.pop('palette_shuffle', False))
            
            ax = kwargs.pop('ax', None)
            if ax is None:
                fig, ax = plt.subplots()
            else:
                fig = ax.figure
            style_kwargs = {k: kwargs.pop(k, None) for k in ['title', 'xlabel', 'ylabel', 'grid', 'data_labels', 'data_label_format',
                                                            'legend_title', 'series_names', 'font_name', 
                                                            'show_legend', 'show_xaxis', 'show_yaxis', 
                                                            'title_fontsize', 'label_fontsize', 'tick_labelsize', 
                                                            'legend_fontsize', 'xtick_format', 'ytick_format', 
                                                            'figsize', 'xlim', 'ylim', 'tick_rotation', 
                                                            'background_color', 'bar_edge_color', 'grid_axis',
                                                            'data_label_position', 'data_label_color', 'data_label_fontsize']}

            plot_kwargs = cls._filter_plot_kwargs(kwargs)
            data.plot(ax=ax, **plot_kwargs)
            cls.apply_chart_style(ax, **style_kwargs)
            plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, ax
        @classmethod
        def scatter(cls, data: 'pd.DataFrame', x: str, y: str, **kwargs) -> Tuple['plt.Figure', 'plt.Axes']:
            """
            Represents data using a scatter plot.

            Args:
                data (pd.DataFrame): Input data as a DataFrame.
                x (str): Column name for the X-axis data.
                y (str): Column name for the Y-axis data.
                title (str): The title of the chart.
                title_fontsize (int): The font size for the title.
                xlabel (str): The label for the X-axis.
                ylabel (str): The label for the Y-axis.
                color_palette (str): Name of a predefined color palette or a custom list of colors. Defaults to 'vnstock'. Available palettes: 'percentage', 'amount', 'category', 'trend', 'flatui', 'vnstock', 'learn_anything'.
                palette_shuffle (bool): Randomize the order of colors in the palette. Defaults to False.
                grid (bool): Displays the grid. True to show, False to hide.
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
            data.plot(kind='scatter', x=x, y=y, ax=ax, **plot_kwargs)
            cls.apply_chart_style(ax, **style_kwargs)
            plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, ax
        @classmethod
        def combo(cls, bar_data: Union['pd.Series', 'pd.DataFrame'], line_data: Union['pd.Series', 'pd.DataFrame'], left_ylabel: str = 'Bar Data', right_ylabel: str = 'Line Data', **kwargs) -> Tuple['plt.Figure', 'plt.Axes', 'plt.Axes']:
            """
            Creates a combo chart with a bar chart and a line chart on two different Y axes.

            Args:
                bar_data (pd.Series): Data for the bar chart.
                line_data (pd.Series): Data for the line chart.
                **kwargs: Additional keyword arguments for styling.
            """
            # Setup figure and primary axis
            fig, ax1 = plt.subplots()
            mpl_plot_instance = cls()
            mpl_plot_instance.utils.apply_palette(kwargs.pop('color_palette', cls._global_theme), kwargs.pop('palette_shuffle', False))

            style_kwargs = {k: kwargs.pop(k, None) for k in ['title', 'xlabel', 'grid', 
                                                            'data_labels', 'data_label_format', 'legend_title', 'series_names', 
                                                            'font_name', 'show_legend', 'show_xaxis', 
                                                            'show_yaxis', 'title_fontsize', 'label_fontsize', 
                                                            'tick_labelsize', 'legend_fontsize', 'xtick_format', 
                                                            'ytick_format', 'figsize', 'xlim', 'ylim', 
                                                            'tick_rotation', 'background_color', 'bar_edge_color', 'grid_axis',
                                                            'data_label_position', 'data_label_color', 'data_label_fontsize']}

            # Get palette colors
            palette_name = kwargs.get('color_palette', 'vnstock')
            palette = Utils.brand_palettes.get(palette_name, Utils.brand_palettes['vnstock'])
            bar_color = palette[0]
            # Use a warm color (index 2 or 3) for contrast, default to a soft orange if available
            line_color = palette[2] if len(palette) > 2 else '#FFB74D' 

            # Bar chart
            plot_kwargs = cls._filter_plot_kwargs(kwargs)
            ax1.bar(bar_data.index, bar_data.values, label=bar_data.name, color=bar_color, **plot_kwargs)
            ax1.set_ylabel(left_ylabel, fontsize=style_kwargs.get('label_fontsize', 10), color=bar_color, fontweight='bold')
        
            # Line chart on secondary axis
            ax2 = ax1.twinx()
            ax2.plot(line_data.index, line_data.values, label=line_data.name, color=line_color, linewidth=2.5, marker='o', markersize=6, **plot_kwargs)
            ax2.set_ylabel(right_ylabel, fontsize=style_kwargs.get('label_fontsize', 10), color=line_color, fontweight='bold')

            # Apply common chart styles
            style_kwargs['grid'] = False
            cls.apply_chart_style(ax1, **style_kwargs)
        
            # Disable grid for ax2 to prevent overlapping
            cls.apply_chart_style(ax2, **style_kwargs)

            # Handle legends
            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left')

            plt.show()
            cls._inject_logo(fig, kwargs)
            return fig, ax1, ax2
        @classmethod
        def timeseries(cls, data, **kwargs):
            import warnings
            warnings.warn("'timeseries' is deprecated. Please use 'line' instead.", DeprecationWarning, stacklevel=2)
            return cls.line(data, **kwargs)
        @classmethod
        def combo_chart(cls, bar_data, line_data, **kwargs):
            import warnings
            warnings.warn("'combo_chart' is deprecated. Please use 'combo' instead.", DeprecationWarning, stacklevel=2)
            return cls.combo(bar_data, line_data, **kwargs)
