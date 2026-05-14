import warnings
from .static.chart import Chart, MPlot
from .utils import Utils
from .config import *

warnings.warn(
    "Importing from `vnstock_ezchart.mplot` is deprecated and will be removed in a future release. "
    "Please import `Chart` directly from `vnstock_ezchart` (e.g., `from vnstock_ezchart import Chart`).",
    DeprecationWarning,
    stacklevel=2
)
