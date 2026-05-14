# Giới thiệu vnstock_ezchart (About vnstock_ezchart)

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

*[English version below](#english-version)*

> **Tầm nhìn:** `vnstock_ezchart` ra đời với sứ mệnh tạo ra **ngôn ngữ trực quan hoá dữ liệu chuyên nghiệp, chuẩn hoá** dành cho cộng đồng đầu tư tại Việt Nam.

Trong bối cảnh số đông nhà đầu tư đang dần tiếp cận với Python và API chứng khoán qua `vnstock`, việc tự viết code hoặc yêu cầu AI vẽ biểu đồ từ con số 0 thường tốn rất nhiều thời gian, tiêu tốn token, và khó duy trì được tính nhất quán về mặt thẩm mỹ. 

Để giải quyết vấn đề đó, `vnstock_ezchart` cung cấp một bộ công cụ tạo biểu đồ tĩnh (static charting) được tinh chỉnh theo triết lý **"Soft Premium"**. Thư viện giúp tự động hóa khâu xử lý thẩm mỹ, định vị thương hiệu (chèn logo), mang lại kết quả đầu ra sẵn sàng để nhúng trực tiếp vào các tài liệu, nghiên cứu, và báo cáo phân tích chuyên nghiệp.

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

### Mã nguồn Khởi tạo Tối giản

Thay vì phải lặp lại thiết lập cấu hình màu sắc hay logo cho từng đồ thị, `vnstock_ezchart` thiết kế cấu trúc Global Theme để bạn chỉ cần khai báo một lần duy nhất.

```python
from vnstock_ezchart import Chart

# 1. Cài đặt Theme, Font & Ngôn ngữ toàn cục (Chỉ chạy 1 lần)
# lang='vi' (mặc định) hoặc lang='en' cho nhãn tiếng Anh
Chart.set_theme(theme_name='vnstock', font_name='Inter', lang='vi')

# 2. Sinh biểu đồ siêu tốc từ dữ liệu pandas (Ví dụ: DataFrame hoặc Series)
fig, ax = Chart.line(data, title="Tăng trưởng Lợi nhuận Hàng quý")
```

---

## 📈 Khả năng Phân tích Đầu tư Chuyên sâu

Lấy cảm hứng từ các nền tảng phân tích định lượng học thuật, `vnstock_ezchart` sở hữu khả năng biến hóa đa dạng để phục vụ vô vàn ngữ cảnh trong tài chính và chứng khoán.

### Phân tích Kỹ thuật Nâng cao & Tâm lý Thị trường
Khả năng "chồng lớp" (Multi-layer) nhiều chiều dữ liệu lên cùng một biểu đồ mà vẫn giữ được sự tinh tế:

<p align="center">
  <img src="./docs/assets/gallery/06_candlestick_advanced.png" width="49%" />
  <img src="./docs/assets/gallery/13_seasonality_boxplot.png" width="49%" />
  <img src="./docs/assets/gallery/12_sentiment_wordcloud.png" width="49%" />
  <img src="./docs/assets/gallery/11_stock_screening_table.png" width="49%" />
</p>

### Quản trị Hiệu suất & Rủi ro
Cung cấp góc nhìn tổ chức (Institutional-grade) về danh mục đầu tư:

<p align="center">
  <img src="./docs/assets/gallery/01_equity_curve.png" width="99%" />
  <img src="./docs/assets/gallery/02_returns_heatmap.png" width="49%" />
  <img src="./docs/assets/gallery/04_rolling_volatility.png" width="49%" />
  <img src="./docs/assets/gallery/05_returns_distribution.png" width="49%" />
  <img src="./docs/assets/gallery/03_yearly_returns.png" width="49%" />
</p>

### Phân bổ & Đánh giá Danh mục
Trực quan hóa cấu trúc danh mục và tương quan thị trường đa lớp tài sản:

<p align="center">
  <img src="./docs/assets/gallery/07_portfolio_treemap.png" width="49%" />
  <img src="./docs/assets/gallery/08_correlation_scatter.png" width="49%" />
  <img src="./docs/assets/gallery/10_multi_asset_line.png" width="49%" />
  <img src="./docs/assets/gallery/14_sectors_pairplot.png" width="49%" />
</p>

### Dữ liệu Thị trường & Phân tích Doanh nghiệp
Khắc họa sâu sắc bức tranh tài chính doanh nghiệp và thanh khoản thị trường:

<p align="center">
  <img src="./docs/assets/gallery/09_fundamental_combo.png" width="99%" />
  <img src="./docs/assets/gallery/18_cash_flow_stacked.png" width="49%" />
  <img src="./docs/assets/gallery/17_financial_ratios.png" width="49%" />
  <img src="./docs/assets/gallery/15_orderbook_volume.png" width="49%" />
  <img src="./docs/assets/gallery/16_foreign_trade.png" width="49%" />
</p>

### Thẻ Tóm tắt Cổ phiếu (Stock Summary Card)
Hiển thị thông tin tóm tắt về cổ phiếu theo thiết kế giao diện UI hiện đại (Soft Premium) tương tự các website tài chính hàng đầu.

<p align="center">
  <img src="./docs/assets/gallery/19_summary_card_positive.png" width="49%" />
  <img src="./docs/assets/gallery/20_summary_card_negative.png" width="49%" />
</p>

### Trực quan hóa Backtesting (Backtesting Visualization)
Cung cấp bộ biểu đồ đầy đủ thông tin cho chiến lược backtest: nến nhật, khối lượng, điểm vào/ra lệnh, đường cong lợi nhuận và drawdown trên cùng một trục thời gian.

<p align="center">
  <img src="./docs/assets/gallery/23_backtest_vi.png" width="99%" />
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

`vnstock_ezchart` provides a suite of static charting tools refined under the **"Soft Premium"** philosophy. It automates aesthetic processing and branding, delivering output ready for professional reports.

---

## 🤖 Agent-Ready Architecture

Optimized for AI Agents with English Google-style Docstrings. Compatible with the [Vnstock Agent Guide](https://github.com/vnstock-hq/vnstock-agent-guide/).

---

## ⚡ Installation & Initialization

```bash
pip install vnstock-ezchart
pip install vnstock-ezchart[all]
```

```python
from vnstock_ezchart import Chart
# 1. Setup Global Theme, Font & Language (Run once)
# lang='vi' (default) or lang='en' for English labels
Chart.set_theme(theme_name='vnstock', font_name='Inter', lang='en')

# 2. Superfast chart generation from pandas data (E.g. DataFrame or Series)
fig, ax = Chart.line(data, title="Quarterly Profit Growth")
```

---

## 📈 Investment Analysis Showcase

### Advanced Technical Analysis & Sentiment
<p align="center">
  <img src="./docs/assets/gallery/06_candlestick_advanced_en.png" width="49%" />
  <img src="./docs/assets/gallery/13_seasonality_boxplot_en.png" width="49%" />
  <img src="./docs/assets/gallery/12_sentiment_wordcloud_en.png" width="49%" />
  <img src="./docs/assets/gallery/11_stock_screening_table_en.png" width="49%" />
</p>

### Performance & Risk Management
<p align="center">
  <img src="./docs/assets/gallery/01_equity_curve_en.png" width="99%" />
  <img src="./docs/assets/gallery/02_returns_heatmap_en.png" width="49%" />
  <img src="./docs/assets/gallery/04_rolling_volatility_en.png" width="49%" />
  <img src="./docs/assets/gallery/05_returns_distribution_en.png" width="49%" />
  <img src="./docs/assets/gallery/03_yearly_returns_en.png" width="49%" />
</p>

### Portfolio Allocation & Evaluation
<p align="center">
  <img src="./docs/assets/gallery/07_portfolio_treemap_en.png" width="49%" />
  <img src="./docs/assets/gallery/08_correlation_scatter_en.png" width="49%" />
  <img src="./docs/assets/gallery/10_multi_asset_line_en.png" width="49%" />
  <img src="./docs/assets/gallery/14_sectors_pairplot_en.png" width="49%" />
</p>

### Market Data & Enterprise Analysis
<p align="center">
  <img src="./docs/assets/gallery/09_fundamental_combo_en.png" width="99%" />
  <img src="./docs/assets/gallery/18_cash_flow_stacked_en.png" width="49%" />
  <img src="./docs/assets/gallery/17_financial_ratios_en.png" width="49%" />
  <img src="./docs/assets/gallery/15_orderbook_volume_en.png" width="49%" />
  <img src="./docs/assets/gallery/16_foreign_trade_en.png" width="49%" />
</p>

### Stock Summary Card
<p align="center">
  <img src="./docs/assets/gallery/19_summary_card_positive_en.png" width="49%" />
  <img src="./docs/assets/gallery/20_summary_card_negative_en.png" width="49%" />
</p>

### Backtesting Visualization
Provides a comprehensive chart for backtesting strategies: candlesticks, volume, entry/exit points, equity curve, and drawdown on a unified timeline.

<p align="center">
  <img src="./docs/assets/gallery/23_backtest_en.png" width="99%" />
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