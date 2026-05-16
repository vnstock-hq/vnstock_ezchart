from typing import Union, List, Optional
from .config import *

class Utils:
    """
    Utility class for customizing and manipulating charts.
    """
    def __init__(self):
        pass

    # Adding brand and thematic color palettes
    brand_palettes = {
        'percentage': ['#D45F5F', '#F3C301', '#FEE3A2', '#ADCACB', '#87C159', '#058240'],
        'amount': [
                    '#E8EDE7',  # Lightest Neutral: Base color, suitable for low amounts
                    '#C4D3D5',  # Slightly Darker Neutral: Bridge between lightest neutral and light blue
                    '#81BECE',  # Light Blue: Starts the transition into deeper colors
                    '#AEDCEA',  # Light Sky Blue: Softens the transition from light to mid blues
                    '#378BA4',  # Mid Blue: Represents a mid-range amount
                    '#2B6C8A',  # Ocean Blue: Intermediate shade, deepens the gradient
                    '#6297B5',  # Soft Blue: Fills gap between mid and deep blues
                    '#036280',  # Deep Blue: Indicates larger amounts
                    '#012E4A',  # Darker Blue: Near-endpoint, for higher amounts
                    '#001D35'   # Deep Ocean: Darkest shade, for the highest amounts
                    ],
        'category': [
                    '#000000',  # Black: Neutral/base color, offers maximum contrast
                    '#8B0000',  # Dark Red: Adds depth to warmer tones, enhances contrast
                    '#F8492E',  # Red/Orange: Bright and vibrant, stands out for attention
                    '#FFC107',  # Amber: Bright yellow/orange, adds vibrancy and contrast
                    '#4CAF50',  # Green: Mid-tone green, introduces a fresh hue for contrast
                    '#00F9F0',  # Cyan: Bright and lively, offers a cool, contrasting hue
                    '#0072BB',  # Blue: Solid, reliable blue for stability and trust
                    '#00457E',  # Dark Blue: Deeper blue, adds sophistication and depth
                    '#5CAEFF',  # Sky Blue: Lighter shade of blue, bridges the gap in cool tones
                    '#FB4C69',  # Pink/Red: Vivid and energetic, finalizes the spectrum with warmth
                    ],
        'trend': [
                    '#017C5E',  # Green variant
                    '#7D916A',  # Greenish gray
                    '#1496BB',  # Blue
                    '#CF90B9',  # Purple
                    '#789BBA',  # Light blue
                    '#D4C1CC',  # Light purple/neutral
                    '#4D5C6F',  # Dark neutral/blue
                    '#F6DDB7',  # Light neutral/orange
                    '#FCAF9F',  # Light orange
                    '#E45332',  # Orange/red
                    '#BB191F'   # Red
                        ],
        'stock': [   # 65% luminant
                    '#70db8f', # Green - Increasing
                    '#ff4d4d', # Red - Decreasing
                    '#c44dff', # Purple - Ceiling
                    '#4ddbff', # Cyan - Floor
                    #  '#3385ff', # Blue
                ],
        'flatui': ['#FEDD78', '#348DC1', '#BA516B', '#4FA487', '#9B59B6', '#613F66'],
        'vnstock': ['#66BB6A', '#64B5F6', '#FFB74D', '#E57373', '#BA68C8', '#90A4AE'],
        'learn_anything': ['#002E5D', '#00FF84', '#FFD700', '#808080'],
        'beach' : ['#217074', '#37745B', '#8B9D77', '#E7EAEF', '#EDC5AB'],
        'forest' : ['#162e1a', '#437a38', '#97b261', '#c5d7d7', '#536b69'],
        'academic' : ['#009E73', '#0072B2', '#E69F00', '#D55E00', '#CC79A7', '#56B4E9', '#000000'], # Semantic order (0: Pos, 1: Pri, 2: Sec, 3: Neg)
        'minimal' : ['#10B981', '#1E293B', '#94A3B8', '#EF4444', '#64748B', '#CBD5E1'] # Modern Nord/Slate Semantic
    }

    @classmethod
    def apply_palette(cls, color_palette: Union[str, List[str]], palette_shuffle: bool = False) -> None:
        """
        Applies a color palette to the current matplotlib/seaborn context.

        Args:
            color_palette (Union[str, List[str]]): The name of a predefined palette or a custom list of hex colors.
            palette_shuffle (bool): If True, shuffles the colors in the palette randomly.
        """
        if isinstance(color_palette, str):
            palette = cls.brand_palettes.get(color_palette, None)
            if palette is None:
                print(f"Palette '{color_palette}' not found. Available palettes: {list(cls.brand_palettes.keys())}")
                return
        else:
            palette = color_palette

        # Ensure palette is a list for shuffling and manipulation
        palette_list = list(palette)

        if palette_shuffle:
            random.shuffle(palette_list)

        sns.set_palette(palette_list)
        plt.rcParams['axes.prop_cycle'] = cycler('color', palette_list)

    @staticmethod
    def readable_format(num: Union[int, float], fmt: Optional[str] = None) -> str:
        """
        Converts a large number into a human-readable string format (e.g., 1.5K, 2.0M).
        
        Args:
            num (Union[int, float]): The number to format.
            fmt (Optional[str]): A custom format string to apply.
            
        Returns:
            str: The formatted human-readable string.
        """
        import pandas as pd
        if pd.isna(num):
            return ""
            
        magnitude = 0
        temp_num = num
        while abs(temp_num) >= 1000:
            magnitude += 1
            temp_num /= 1000.0
            
        suffix = ["", "K", "M", "B", "T"][magnitude]
        if fmt and isinstance(fmt, str):
            try:
                # If percentage, use original num without K/M/B scaling
                if '%' in fmt:
                    return fmt.format(num)
                return fmt.format(temp_num) + suffix
            except Exception:
                pass
        return f'{temp_num:.1f}{suffix}'

    @staticmethod
    def list_font() -> pd.Series:
        """
        Lists all fonts currently recognized by Matplotlib. Useful for selecting
        available fonts, especially in cloud environments like Google Colab.
        
        Returns:
            pd.Series: A pandas Series containing the names of all available fonts.
        """
        font_list = []
        for font in font_manager.fontManager.ttflist:
            font_list.append(font.name)

        return pd.Series(font_list)

    @staticmethod
    def download_font(font_family: str) -> None:
        """
        Downloads a font from Google Fonts and registers it with Matplotlib.

        Args:
            font_family (str): The exact font family name as it appears on Google Fonts.
        """
        font_url = f'https://fonts.google.com/download?family={font_family.replace(" ", "+")}'
        response = requests.get(font_url, allow_redirects=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download font: {font_family}")
        zip_path = os.path.join('fonts', f'{font_family}.zip')
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)

        with open(zip_path, 'wb') as font_file:
            font_file.write(response.content)

        extract_dir = os.path.join('fonts', font_family)
        shutil.unpack_archive(zip_path, extract_dir)
        os.remove(zip_path)

        # Add the font to matplotlib's font list
        for root, dirs, files in os.walk(os.path.join('fonts', font_family)):
            for file in files:
                if file.endswith('.ttf'):
                    font_path = os.path.join(root, file)
                    print(font_path)
                    font_manager.fontManager.addfont(font_path)
                    plt.rcParams['font.family'] = font_family

    @staticmethod
    def set_font(font_family: str) -> None:
        """
        Overrides the global Matplotlib font family setting.
        Useful when the environment (like Colab) does not have the desired font.
        
        Args:
            font_family (str): The name of the font family to apply globally.
        """
        plt.rcParams['font.family'] = font_family

    @staticmethod
    def list_cmap() -> pd.Series:
        """
        Lists all available colormaps (cmaps) registered in Matplotlib.
        
        Returns:
            pd.Series: A pandas Series containing the names of available cmaps.
        """
        import matplotlib.pyplot as plt
        return pd.Series(plt.cm.datad)
    
    @classmethod
    def create_cmap(cls, color_palette: Union[str, List[str]], cmap_name: str = 'custom'):
        """
        Creates and registers a custom Matplotlib colormap from a list of colors.
        
        Args:
            color_palette (Union[str, List[str]]): The name of a predefined palette or a list of hex codes.
            cmap_name (str): The name to assign to the newly created colormap.
            
        Returns:
            matplotlib.colors.LinearSegmentedColormap: The generated colormap object.
        """
        from matplotlib.colors import LinearSegmentedColormap

        if isinstance(color_palette, str):
            palette = cls.brand_palettes.get(color_palette, None)
            color_map = LinearSegmentedColormap.from_list(cmap_name, palette, N=len(color_palette))
            if palette is None:
                print(f"Palette '{color_palette}' not found. Available palettes: {list(cls.brand_palettes.keys())}")
                return
        else:
            color_map = LinearSegmentedColormap.from_list(cmap_name, color_palette, N=len(color_palette))
        return color_map