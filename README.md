# 🎯 Engineer Broker - Peter Lynch Investment Analyzer

A web application that automates investment analysis based on **Peter Lynch's methodology** ("One Up on Wall Street"), using AI (**Groq - Llama 3.3**) to generate investment verdicts with intelligent analysis.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Features

- **📊 Real-time Data**: Fetches updated financial metrics via Yahoo Finance
- **📈 Peter Lynch Chart**: Dynamic Fair Value Band visualization with price vs. earnings comparison
- **🎯 Fair Value Band**: Shaded area between optimistic (historical P/E) and conservative (PEG=1) valuations
- **🧠 AI Analysis**: Automatic verdict using **Groq (Llama 3.3 70B)** with "Engineer Broker" personality
- **⚡ Ultra Fast**: Groq offers the fastest AI responses on the market
- **📰 Scuttlebutt**: Displays latest company news
- **🔄 Auto Classification**: Detects if company is Fast Grower, Stalwart, Cyclical, Turnaround, or Asset Play
- **💰 Accurate PEG Calculation**: Uses Yahoo Finance's `trailingPegRatio` with 5-year growth estimates
- **📊 1-Year Projection**: Forward EPS-based projection with smooth interpolation
- **🌐 Bilingual**: Full support for English and Spanish

## 📋 Prerequisites

- Python 3.9 or higher
- Internet connection
- Groq API Key (**100% FREE**)

## 🔑 Get Groq API Key (FREE)

1. Go to [Groq Console](https://console.groq.com/keys)
2. Create a free account (you can use your Google account)
3. Click **"Create API Key"**
4. Name your key and copy it
5. Done! Use it in the application

> **Generous Free Limits:**
> - ✅ **30 requests/minute**
> - ✅ **14,400 requests/day**
> - ✅ No credit card required
> - ✅ Access to **Llama 3.3 70B** model (one of the best open source models)

## ⚙️ Installation

### 1. Clone or download the project

```bash
cd FinancialApp
```

### 2. Create virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

```bash
python -m streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

> **Note**: On Windows, use `python -m streamlit run app.py` instead of just `streamlit run app.py` to avoid PATH issues.

## 📖 How to Use

1. **Enter your Groq API Key** in the left sidebar
2. **Type a ticker** in the search field (e.g., `AAPL`, `MSFT`, `KO`, `V`)
3. **Click "Analyze"** or use the example buttons
4. **Review the results**:
   - Lynch classification badge (Fast Grower, Stalwart, Cyclical, etc.)
   - PEG Ratio calculated with 5-year growth
   - Main metrics panel (price, P/E, PEG, dividend)
   - **Peter Lynch Chart** with Fair Value Band
   - Latest news
   - Complete Engineer Broker analysis with BUY/SELL/HOLD verdict

## 📊 Peter Lynch Chart

The chart displays three key elements:

| Element | Color | Description |
|---------|-------|-------------|
| **Price Line** | 🟢 Green | Current stock price |
| **Fair Value (Upper)** | 🟠 Orange | EPS × Historical Median P/E |
| **Conservative (Lower)** | 🔵 Blue-Gray | EPS × PEG=1 Multiplier (growth-based, floor 15, cap 25) |
| **Fair Value Band** | Shaded | Area between Fair Value and Conservative lines |

**Interpretation:**
- Price **inside** the band = Fair valuation
- Price **above** the band = Potentially overvalued
- Price **below** the band = Potentially undervalued (opportunity)

### Example Tickers

| Ticker | Company | Exchange |
|--------|---------|----------|
| AAPL | Apple | NASDAQ |
| MSFT | Microsoft | NASDAQ |
| KO | Coca-Cola | NYSE |
| TSLA | Tesla | NASDAQ |
| V | Visa | NYSE |
| PG | Procter & Gamble | NYSE |
| DUOL | Duolingo | NASDAQ |
| IBE.MC | Iberdrola | Madrid |
| SAP.DE | SAP | Frankfurt |

## 📊 Metrics Analyzed

The application fetches and analyzes over 40 financial metrics:

- **Valuation**: P/E (Trailing/Forward), **PEG Ratio**, Price/Book, Price/Sales
- **Dividends**: Yield, Annual Rate, Payout Ratio, 5-Year Average
- **Balance Sheet**: Total Debt, Cash, Debt/Equity Ratio, Debt/Cash
- **Profitability**: ROE, ROA, Margins (profit, operating)
- **Growth**: Earnings, Revenue, Forward EPS, Quarterly Growth
- **Risk**: Beta, Volatility

### 🎯 Enhanced PEG Ratio

The PEG is calculated using:
1. **`trailingPegRatio`** from Yahoo Finance (uses 5-year growth estimates from analysts)
2. **Manual calculation** with Forward EPS Growth if not available
3. Shows **detailed calculation** when hovering over the help symbol (?)

## 🎯 Peter Lynch Methodology

The "Engineer Broker" applies the following rules:

### PEG Ratio (Price/Earnings to Growth)
- 🟢 **PEG < 1.0**: Stock is cheap relative to its growth
- 🟡 **PEG 1.0 - 2.0**: Fair valuation
- 🔴 **PEG > 2.0**: Stock is expensive

### Company Classification
- 🚀 **Fast Grower**: High growth, reinvests profits
- 🏛️ **Stalwart**: Large companies, moderate growth, dividends
- 🔄 **Cyclical**: Depends on economic cycle
- 📈 **Turnaround**: In restructuring process
- 💎 **Asset Play**: Unrecognized value on balance sheet

### Debt Analysis
- ✅ More cash than debt = Solid position
- ⚠️ More debt than cash = Caution needed

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.28+
- **Financial Data**: yfinance (Yahoo Finance API)
- **Charts**: Plotly (interactive with zoom and hover)
- **AI**: Groq API with **Llama 3.3 70B Versatile**
- **Processing**: Pandas, NumPy
- **Language**: Python 3.9+

### Why Groq?

| Feature | Groq | Google Gemini |
|---------|------|---------------|
| **Speed** | ⚡ Ultra fast (< 1s) | Normal (2-5s) |
| **Free Limits** | 14,400 req/day | ~60 req/day |
| **Quality** | Llama 3.3 70B | Gemini Flash |
| **No Restrictions** | ✅ | ❌ Many |

## ⚠️ Disclaimer

**This software is for educational and informational purposes only.**

- It does not constitute financial, investment, or tax advice
- Analysis results are AI-generated and may contain errors
- Always do your own research (DYOR)
- Consult with a professional financial advisor before investing
- Past performance does not guarantee future results

## 📄 License

MIT License - Feel free to use, modify, and distribute.

## 🤝 Contributions

Contributions are welcome. Please open an issue first to discuss significant changes.

## 🐛 Known Issues and Solutions

### Error: "streamlit is not recognized as a command"
**Solution**: Use `python -m streamlit run app.py` instead of `streamlit run app.py`

### PEG Ratio shows N/A
PEG requires Yahoo Finance to have growth data. Some small or new companies may not have this information available.

### Dividend Yield shows N/A
Companies that don't pay dividends (like many growth tech companies) will show N/A. This is normal.

---

**Developed with ❤️ inspired by Peter Lynch's investment philosophy**

*"Invest in what you know"* - Peter Lynch
