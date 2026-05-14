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

from ..core.style import StyleMixin
from .basic import BasicMixin
from .financial import FinancialMixin
from .statistical import StatisticalMixin
from .specialized import SpecializedMixin
from .quant import QuantMixin
import warnings

class Chart(StyleMixin, BasicMixin, FinancialMixin, StatisticalMixin, SpecializedMixin, QuantMixin):
    """
    Core static charting library for investment analysis.
    Provides methods to draw modern, AI-agent compatible charts using Matplotlib and Seaborn.
    """
    def __init__(self):
        """Initialize the Chart object."""
        self.utils = Utils()

class MPlot(Chart):
    """
    Deprecated alias for Chart. Maintained for backward compatibility.
    Please use `Chart` instead.
    """
    def __init__(self):
        warnings.warn(
            "MPlot is deprecated and will be removed in a future release. Please use `Chart` instead.", 
            DeprecationWarning, 
            stacklevel=2
        )
        super().__init__()
