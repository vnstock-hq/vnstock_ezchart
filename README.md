# Giới thiệu vnstock_ezchart

<div id="logo" align="center">
    <a href="http://vnstock.site?utm_source=vnstock_docs&utm_medium=start&utm_content=logo">
        <img src="https://raw.githubusercontent.com/thinh-vu/vnstock/beta/docs/docs/assets/images/vnstock_logo_color.png" alt="vnstock_logo"/>
    </a>
</div>

---

<div id="badges" align="center">
<img src="https://img.shields.io/pypi/pyversions/vnstock_ezchart?logoColor=brown&style=plastic" alt= "Version"/>
<img src="https://img.shields.io/pypi/dm/vnstock_ezchart" alt="Download Badge"/>
<img src="https://img.shields.io/github/last-commit/vnstock-hq/vnstock_ezchart" alt="Commit Badge"/>
<img src="https://img.shields.io/github/license/vnstock-hq/vnstock_ezchart?color=red" alt="License Badge"/>
</div>

*🌐 [English version below](#english-version)*

> **Tầm nhìn:** `vnstock_ezchart` ra đời với sứ mệnh tạo ra **ngôn ngữ trực quan hoá dữ liệu chuyên nghiệp, chuẩn hoá** dành cho cộng đồng đầu tư tại Việt Nam.

Trong bối cảnh số đông nhà đầu tư đang dần tiếp cận với Python và API chứng khoán qua `vnstock`, việc tự viết code hoặc yêu cầu AI vẽ biểu đồ từ con số 0 thường tốn rất nhiều thời gian, tiêu tốn token, và khó duy trì được tính nhất quán về mặt thẩm mỹ. 

**Tại sao lại là biểu đồ tĩnh (Static Charting)?**
`vnstock_ezchart` tập trung tối đa vào việc tạo ra các biểu đồ tĩnh để giải quyết triệt để các bài toán thực tiễn:
1. **Nghiên cứu & Học thuật:** Kết xuất ảnh với độ nét cao, dễ dàng nhúng trực tiếp vào các báo cáo phân tích, tài liệu in ấn mà không bị vỡ nét hay phụ thuộc vào trình duyệt web.
2. **Tự động hoá phân tích đầu tư:** Hỗ trợ xuất ảnh để tự động gửi báo cáo danh mục, phân tích kỹ thuật hay tín hiệu giao dịch cho khách hàng/nhà đầu tư qua các nền tảng chat (Telegram, Discord, Zalo). Dễ dàng tích hợp tự động hóa qua Openclaw hoặc bất kỳ AI Agent nào.
3. **Phân tích Thị giác bằng AI:** Khi cung cấp biểu đồ tĩnh cho các AI Agent (ví dụ trong Google Antigravity hay các IDE khác), bản thân AI có thể "nhìn" và đọc hiểu hình ảnh biểu đồ giống hệt cách con người trải nghiệm. Điều này giúp AI đưa ra những nhận định, phân tích đáng tin cậy dựa trên mặt hình ảnh thay vì chỉ đọc các con số.

Thư viện giúp tự động hóa toàn bộ khâu xử lý thẩm mỹ và định vị thương hiệu (chèn logo), mang lại kết quả đầu ra sẵn sàng sử dụng ngay lập tức cho các báo cáo phân tích chuyên nghiệp.

---

## 🤖 Kiến trúc Agent-Ready

Thư viện được thiết kế tối ưu hóa 100% cho khả năng tương tác với AI Agent. Các hàm vẽ biểu đồ sử dụng Docstrings chuẩn Google-style bằng tiếng Anh, giúp các Agent hiểu rõ ngữ nghĩa và cú pháp ngay lập tức.
Bạn có thể kết hợp thư viện này hoàn hảo với hệ sinh thái AI thông qua bộ tài liệu [Vnstock Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/).

---

## ⚡ Cài đặt & Khởi tạo

```bash
# Cài đặt thư viện mặc định
pip install vnstock-ezchart

# Cài đặt thêm các thành phần bổ trợ (Treemap, Wordcloud)
pip install vnstock-ezchart[all]
```

### Khởi tạo & Tuỳ biến Giao diện (Theming & Branding)

Thay vì phải lặp lại thiết lập màu sắc hay logo cho từng đồ thị, `vnstock_ezchart` hỗ trợ cấu trúc Global Theme giúp bạn chỉ cần khai báo một lần duy nhất.

#### 1. Sử dụng Theme có sẵn
Thư viện cung cấp sẵn nhiều bộ theme chuyên nghiệp: `vnstock` (Soft Premium), `academic` (Báo cáo khoa học), `minimal` (Tối giản hiện đại), `flatui`, v.v.
```python
from vnstock_ezchart import Chart

# Cài đặt Theme, Font & Ngôn ngữ toàn cục
Chart.set_theme(theme_name='vnstock', font_name='Inter', lang='vi')
```

#### 2. Tự định nghĩa Theme màu sắc (Custom Palette)
Bạn hoàn toàn có thể tự tạo bộ màu mang bản sắc riêng bằng cách đăng ký vào `Utils.brand_palettes`. Hãy chú ý đến tính Ngữ nghĩa (Semantic) của thứ tự màu:
- **Index 0**: Màu Tích cực / Tăng trưởng (VD: Xanh lá)
- **Index 1**: Màu Dữ liệu chính
- **Index 2**: Màu Phụ trợ / Cảnh báo (VD: Vàng/Cam)
- **Index 3**: Màu Tiêu cực / Giảm điểm (VD: Đỏ)

```python
from vnstock_ezchart.utils import Utils

# Định nghĩa Theme mới
Utils.brand_palettes['my_theme'] = ['#10B981', '#1E293B', '#F59E0B', '#EF4444', '#64748B', '#CBD5E1']

# Kích hoạt Theme vừa tạo
Chart.set_theme(theme_name='my_theme', lang='vi')
```

#### 3. Thay đổi Logo Watermark thương hiệu
Thư viện cho phép bạn tự do thay thế Watermark mặc định bằng logo của cá nhân/doanh nghiệp:

```python
# Thay thế logo toàn cục bằng đường dẫn file hoặc URL
Chart.set_logo("https://your-domain.com/path/to/your/logo.png")

# Tắt hoàn toàn logo
Chart.set_logo(None)
```

---

## 📈 Khả năng Phân tích Đầu tư Chuyên sâu

Lấy cảm hứng từ các nền tảng phân tích định lượng học thuật, `vnstock_ezchart` sở hữu khả năng biến hóa đa dạng để phục vụ vô vàn ngữ cảnh trong tài chính và chứng khoán.

### Phân tích Kỹ thuật Nâng cao & Tâm lý Thị trường

Khả năng "chồng lớp" (Multi-layer) nhiều chiều dữ liệu lên cùng một biểu đồ mà vẫn giữ được sự tinh tế:

<p align="center">
  <img src="./docs/assets/gallery/vnstock/vi/06_candlestick_advanced.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/13_seasonality_boxplot.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/12_sentiment_wordcloud.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/11_stock_screening_table.png" width="49%" />
</p>

### Thư viện Chỉ báo Kỹ thuật Đa dạng

Hỗ trợ trực quan hóa sinh động hàng chục chỉ báo phân tích kỹ thuật phổ biến với độ tuỳ biến cao, dễ dàng tùy chỉnh màu sắc, vùng tô (fill) và các lớp thông tin (overlays). Hỗ trợ hoàn hảo ngay cả những chỉ báo phức tạp đa chiều (như Ichimoku, Bollinger Bands, MACD, Donchian Channels v.v.):

<p align="center">
  <img src="./docs/assets/gallery/vnstock/vi/indicator_trend_ichimoku.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/indicator_momentum_macd.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/indicator_volatility_bbands.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/indicator_volatility_donchian.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/indicator_momentum_stochrsi.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/indicator_trend_supertrend.png" width="49%" />
</p>

### Quản trị Hiệu suất & Rủi ro

Cung cấp góc nhìn tổ chức (Institutional-grade) về danh mục đầu tư:

<p align="center">
  <img src="./docs/assets/gallery/vnstock/vi/01_equity_curve.png" width="99%" />
  <img src="./docs/assets/gallery/vnstock/vi/02_returns_heatmap.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/04_rolling_volatility.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/05_returns_distribution.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/03_yearly_returns.png" width="49%" />
</p>

### Phân bổ & Đánh giá Danh mục

Trực quan hóa cấu trúc danh mục và tương quan thị trường đa lớp tài sản:

<p align="center">
  <img src="./docs/assets/gallery/vnstock/vi/07_portfolio_treemap.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/08_correlation_scatter.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/10_multi_asset_line.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/14_sectors_pairplot.png" width="49%" />
</p>

### Dữ liệu Thị trường & Phân tích Doanh nghiệp

Khắc họa sâu sắc bức tranh tài chính doanh nghiệp và thanh khoản thị trường:

<p align="center">
  <img src="./docs/assets/gallery/vnstock/vi/09_fundamental_combo.png" width="99%" />
  <img src="./docs/assets/gallery/vnstock/vi/18_cash_flow_stacked.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/17_financial_ratios.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/15_orderbook_volume.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/16_foreign_trade.png" width="49%" />
</p>

### Thẻ Tóm tắt Cổ phiếu (Stock Summary Card)

Hiển thị thông tin tóm tắt về cổ phiếu theo thiết kế giao diện UI hiện đại (Soft Premium) tương tự các website tài chính hàng đầu.

<p align="center">
  <img src="./docs/assets/gallery/vnstock/vi/19_summary_card_positive.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/vi/20_summary_card_negative.png" width="49%" />
</p>


### Đa Dạng Theme Thiết Kế (Multi-Theme Support)

Thư viện hỗ trợ nhiều theme phù hợp với các ngữ cảnh ứng dụng khác nhau. Ví dụ dưới đây là sự khác biệt giữa theme `vnstock` (Soft Premium), `academic` (chuẩn báo cáo khoa học), và `minimal` (tối giản):

<p align="center">
  <img src="./docs/assets/gallery/vnstock/vi/06_candlestick_advanced.png" width="32%" />
  <img src="./docs/assets/gallery/academic/vi/06_candlestick_advanced.png" width="32%" />
  <img src="./docs/assets/gallery/minimal/vi/06_candlestick_advanced.png" width="32%" />
</p>

### Trực quan hóa Backtesting (Backtesting Visualization)

Cung cấp bộ biểu đồ đầy đủ thông tin cho chiến lược backtest: nến nhật, khối lượng, điểm vào/ra lệnh, đường cong lợi nhuận và drawdown trên cùng một trục thời gian.

<p align="center">
  <img src="./docs/assets/gallery/vnstock/vi/23_backtest.png" width="99%" />
</p>

---

## 📂 Example Gallery - Bộ Sưu Tập Kịch Bản Chuyên Nghiệp

Mã nguồn mẫu đã được chia nhỏ thành các nhóm ứng dụng riêng biệt giúp bạn dễ dàng theo dõi, bảo trì và sử dụng:

- **[`examples/01_performance_risk.py`](examples/01_performance_risk.py):** Quản trị Hiệu suất & Rủi ro.
- **[`examples/02_technical_analysis.py`](examples/02_technical_analysis.py):** Phân tích Kỹ thuật.
- **[`examples/03_portfolio_management.py`](examples/03_portfolio_management.py):** Phân bổ Danh mục.
- **[`examples/04_market_data.py`](examples/04_market_data.py):** Dữ liệu Thị trường.
- **[`examples/05_enterprise_analysis.py`](examples/05_enterprise_analysis.py):** Phân tích Doanh nghiệp.
- **[`examples/06_summary_cards.py`](examples/06_summary_cards.py):** Thẻ Tóm tắt Cổ phiếu.
- **[`examples/07_backtest.py`](examples/07_backtest.py):** Trực quan hóa kiểm thử - Backtesting.

Bạn có thể chạy toàn bộ các kịch bản để sinh ảnh song ngữ (VI & EN):

```bash
python3 examples/run_all.py
```

---

<a id="english-version"></a>
# English Version

> **Vision:** `vnstock_ezchart` aims to provide a **standardized and professional data visualization language** for the Vietnamese investment community.

As more investors adopt Python and stock APIs via `vnstock`, writing code or asking AI to draw charts from scratch often takes significant time, consumes tokens, and struggles to maintain aesthetic consistency.

**Why Static Charting?**
`vnstock_ezchart` focuses extensively on generating static charts under the **"Soft Premium"** design philosophy to solve real-world practical problems:
1. **Academic & Research:** Export high-resolution images that are easily embedded directly into analysis reports, academic papers, or printed documents without pixelation or browser dependencies.
2. **Real-world Automated Investing:** Export charts to automatically send portfolio reports, technical analysis, or trading signals to clients and investors via chat platforms (Telegram, Discord, Zalo) by integrating with Openclaw or any AI Agent.
3. **AI Vision Analysis:** When static charts are provided to AI Agents (within Antigravity or other IDEs), the AI can "see" and interpret the charts exactly as a human experiences them visually. This enables the AI to provide highly reliable, visually-grounded analysis and insights rather than just reading dry data points.

The library automates all aesthetic processing and branding (logo insertion), delivering an output that is immediately ready for professional reports!

---

## 🤖 Agent-Ready Architecture

Optimized for AI Agents with English Google-style Docstrings. Compatible with the [Vnstock Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/).

---

## ⚡ Installation & Initialization

```bash
pip install vnstock-ezchart
pip install vnstock-ezchart[all]
```

### Theming & Branding Initialization

Instead of repeating color or logo configurations for each chart, `vnstock_ezchart` supports a Global Theme architecture so you only need to declare it once.

#### 1. Using Built-in Themes
The library provides several professional themes out of the box: `vnstock` (Soft Premium), `academic` (Scientific Reports), `minimal` (Modern Slate), `flatui`, etc.
```python
from vnstock_ezchart import Chart

# Setup Global Theme, Font & Language
Chart.set_theme(theme_name='vnstock', font_name='Inter', lang='en')
```

#### 2. Defining Custom Color Palettes
You can create your own brand identity by registering a custom palette to `Utils.brand_palettes`. Please pay attention to the Semantic ordering of the colors:
- **Index 0**: Positive / Up Color (e.g., Green)
- **Index 1**: Primary Data Color
- **Index 2**: Secondary / Warning Color (e.g., Yellow/Orange)
- **Index 3**: Negative / Down Color (e.g., Red)

```python
from vnstock_ezchart.utils import Utils

# Define new custom theme
Utils.brand_palettes['my_theme'] = ['#10B981', '#1E293B', '#F59E0B', '#EF4444', '#64748B', '#CBD5E1']

# Activate the new theme
Chart.set_theme(theme_name='my_theme', lang='en')
```

#### 3. Replacing the Brand Watermark Logo
The library allows you to freely replace the default watermark with your own personal or corporate logo:

```python
# Replace global logo using a file path or URL
Chart.set_logo("https://your-domain.com/path/to/your/logo.png")

# Completely disable the logo
Chart.set_logo(None)
```

---

## 📈 Investment Analysis Showcase

### Advanced Technical Analysis & Sentiment

<p align="center">
  <img src="./docs/assets/gallery/vnstock/en/06_candlestick_advanced.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/13_seasonality_boxplot.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/12_sentiment_wordcloud.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/11_stock_screening_table.png" width="49%" />
</p>

### Comprehensive Technical Indicators Library

Supports visualizing dozens of popular technical analysis indicators with high customizability, easily adjusting colors, fill areas, and overlays. Perfectly handles complex, multi-dimensional indicators (such as Ichimoku, Bollinger Bands, MACD, Donchian Channels, etc.):

<p align="center">
  <img src="./docs/assets/gallery/vnstock/en/indicator_trend_ichimoku.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/indicator_momentum_macd.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/indicator_volatility_bbands.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/indicator_volatility_donchian.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/indicator_momentum_stochrsi.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/indicator_trend_supertrend.png" width="49%" />
</p>

### Performance & Risk Management

<p align="center">
  <img src="./docs/assets/gallery/vnstock/en/01_equity_curve.png" width="99%" />
  <img src="./docs/assets/gallery/vnstock/en/02_returns_heatmap.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/04_rolling_volatility.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/05_returns_distribution.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/03_yearly_returns.png" width="49%" />
</p>

### Portfolio Allocation & Evaluation

<p align="center">
  <img src="./docs/assets/gallery/vnstock/en/07_portfolio_treemap.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/08_correlation_scatter.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/10_multi_asset_line.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/14_sectors_pairplot.png" width="49%" />
</p>

### Market Data & Enterprise Analysis

<p align="center">
  <img src="./docs/assets/gallery/vnstock/en/09_fundamental_combo.png" width="99%" />
  <img src="./docs/assets/gallery/vnstock/en/18_cash_flow_stacked.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/17_financial_ratios.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/15_orderbook_volume.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/16_foreign_trade.png" width="49%" />
</p>

### Stock Summary Card

<p align="center">
  <img src="./docs/assets/gallery/vnstock/en/19_summary_card_positive.png" width="49%" />
  <img src="./docs/assets/gallery/vnstock/en/20_summary_card_negative.png" width="49%" />
</p>


### Multi-Theme Support

The library supports multiple themes tailored for different application contexts. Below is a comparison between the `vnstock` (Soft Premium) theme, the `academic` theme (for scientific reports), and the `minimal` theme:

<p align="center">
  <img src="./docs/assets/gallery/vnstock/en/06_candlestick_advanced.png" width="32%" />
  <img src="./docs/assets/gallery/academic/en/06_candlestick_advanced.png" width="32%" />
  <img src="./docs/assets/gallery/minimal/en/06_candlestick_advanced.png" width="32%" />
</p>

### Backtesting Visualization

Provides a comprehensive chart for backtesting strategies: candlesticks, volume, entry/exit points, equity curve, and drawdown on a unified timeline.

<p align="center">
  <img src="./docs/assets/gallery/vnstock/en/23_backtest.png" width="99%" />
</p>

---

## 📂 Example Gallery - Professional Scenario Collection

The sample source code has been broken down into separate application groups, making it easy for you to track, maintain, and use:

- **[`examples/01_performance_risk.py`](examples/01_performance_risk.py):** Performance & Risk Management.
- **[`examples/02_technical_analysis.py`](examples/02_technical_analysis.py):** Technical Analysis.
- **[`examples/03_portfolio_management.py`](examples/03_portfolio_management.py):** Portfolio Allocation.
- **[`examples/04_market_data.py`](examples/04_market_data.py):** Market Data.
- **[`examples/05_enterprise_analysis.py`](examples/05_enterprise_analysis.py):** Enterprise Analysis.
- **[`examples/06_summary_cards.py`](examples/06_summary_cards.py):** Stock Summary Card.
- **[`examples/07_backtest.py`](examples/07_backtest.py):** Backtesting Visualization.

You can run all the scripts above simultaneously to output the bilingual image collection:

```bash
python3 examples/run_all.py
```