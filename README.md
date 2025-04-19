# 📈 Intrinsic Value Alert System
This project is a Python-based tool for estimating the intrinsic value of selected stocks using a DCF (Discounted Cash Flow) model, comparing it to the current market price, and providing buy/sell/fair signals.

## ✅ Current Features
- Accepts a CSV file of tickers with optional override parameters (growth rate, discount rate, etc.)
- Uses yfinance to fetch financial data
- Performs a DCF valuation
- Outputs valuation results and investment suggestions to the console
- Fully modular with Python 3.9+ compatibility
- Requirements listed in requirements.txt

## 📋 To-Do List
#### 🔄 Position Timing Logic
 - Determine time horizon for each buy/sell signal
 - Define stop-loss and profit-taking thresholds
 - Add logic to minimize false signals or reduce estimation error

#### 🕒 Scheduled Tracking & Backtesting
 - Build a scheduled job (e.g., with cron, schedule, or APScheduler)
 - Track selected "test" stocks multiple times per trading day
 - Save tracking results (price, valuation, signal) to CSV, SQLite, or another data store
 - Create a script or notebook to analyze performance and accuracy of historical signals

## 🔧 Coming Soon
 - Slack or WhatsApp integration for real-time alerts
 - Web interface or dashboard (e.g., Streamlit)
 - Automated screening of large stock lists

## 🛠 Requirements
Install dependencies:
```
pip install -r requirements.txt
```

**Python version: 3.9+**
