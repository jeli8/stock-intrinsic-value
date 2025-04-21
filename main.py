import pandas as pd
from evaluator import fetch_financials
from dcf_model import dcf_valuation
from config import *
from datetime import datetime
import csv
import os

def load_tickers(filename):
    return pd.read_csv(filename)

def get_results_filename():
    date_str = datetime.now().strftime('%Y-%m-%d')
    return f'results_{date_str}.csv'

def calculate_trading_thresholds(current_price, intrinsic_value):
    """Calculate stop-loss and profit-taking thresholds based on intrinsic value and current price"""
    # If stock is undervalued (potential buy)
    if intrinsic_value > current_price:
        stop_loss = current_price * 0.90  # 10% below entry point
        profit_target = min(intrinsic_value * 1.1, current_price * 1.30)  # Either 10% above intrinsic or 30% above entry
        action = "BUY"
    # If stock is overvalued (potential sell)
    elif intrinsic_value < current_price:
        stop_loss = current_price * 0.95  # 5% below current price for existing positions
        profit_target = current_price * 1.05  # 5% above current price to exit
        action = "SELL"
    # If fairly valued
    else:
        stop_loss = intrinsic_value * 0.90  # 10% below intrinsic value
        profit_target = intrinsic_value * 1.10  # 10% above intrinsic value
        action = "HOLD"
    
    return stop_loss, profit_target, action

def evaluate_stock(row, results):
    ticker = row['ticker']
    data = fetch_financials(ticker)
    if not data:
        return

    # Use overrides or defaults
    growth = row['growth_rate'] if pd.notna(row['growth_rate']) else DEFAULT_GROWTH_RATE
    discount = row['discount_rate'] if pd.notna(row['discount_rate']) else DEFAULT_DISCOUNT_RATE
    years = int(row['years']) if pd.notna(row['years']) else DEFAULT_YEARS
    terminal = row['terminal_growth'] if pd.notna(row['terminal_growth']) else DEFAULT_TERMINAL_GROWTH

    intrinsic_value = dcf_valuation(
        fcf=data["fcf"],
        growth_rate=growth,
        discount_rate=discount,
        years=years,
        terminal_growth=terminal
    )

    intrinsic_per_share = intrinsic_value / data["shares"]
    current_price = data["price"]
    
    # Calculate trading thresholds
    stop_loss, profit_target, action = calculate_trading_thresholds(current_price, intrinsic_per_share)
    
    # Calculate value metrics
    value_gap = ((intrinsic_per_share - current_price) / current_price) * 100
    risk_reward = (profit_target - current_price) / (current_price - stop_loss) if stop_loss < current_price else 0

    # Determine valuation signal with more detail
    if intrinsic_per_share > current_price * 1.2:
        signal = f"Undervalued (Strong Buy) - {value_gap:.1f}% below intrinsic value"
    elif intrinsic_per_share < current_price * 0.8:
        signal = f"Overvalued (Strong Sell) - {-value_gap:.1f}% above intrinsic value"
    else:
        signal = f"Fairly valued (Hold) - {abs(value_gap):.1f}% from intrinsic value"

    # Print to console
    print(f"\n{data['name']} ({ticker})")
    print(f"  Current Price: ${current_price:.2f}")
    print(f"  Intrinsic Value: ${intrinsic_per_share:.2f}")
    print(f"  -> {signal}")
    print(f"  Stop Loss: ${stop_loss:.2f}")
    print(f"  Profit Target: ${profit_target:.2f}")
    print(f"  Risk/Reward Ratio: {risk_reward:.2f}")

    # Add to results
    results.append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'name': data['name'],
        'ticker': ticker,
        'current_price': f"${current_price:.2f}",
        'intrinsic_value': f"${intrinsic_per_share:.2f}",
        'value_gap_percent': f"{value_gap:.1f}%",
        'stop_loss': f"${stop_loss:.2f}",
        'profit_target': f"${profit_target:.2f}",
        'risk_reward': f"{risk_reward:.2f}",
        'action': action,
        'valuation_signal': signal
    })

if __name__ == "__main__":
    results = []
    df = load_tickers(CSV_FILE)
    
    for _, row in df.iterrows():
        evaluate_stock(row, results)
    
    # Save results to CSV
    filename = get_results_filename()
    fieldnames = ['date', 'name', 'ticker', 'current_price', 'intrinsic_value', 
                 'value_gap_percent', 'stop_loss', 'profit_target', 'risk_reward', 
                 'action', 'valuation_signal']
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nResults saved to {filename}")
