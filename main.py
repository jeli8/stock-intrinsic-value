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

    # Determine valuation signal
    if intrinsic_per_share > current_price * 1.2:
        signal = "Undervalued (Buy signal)"
    elif intrinsic_per_share < current_price * 0.8:
        signal = "Overvalued (Sell signal)"
    else:
        signal = "Fairly valued"

    # Print to console (keeping original output)
    print(f"\n{data['name']} ({ticker})")
    print(f"  Current Price: ${current_price:.2f}")
    print(f"  Intrinsic Value: ${intrinsic_per_share:.2f}")
    print(f"  -> {signal}")

    # Add to results
    results.append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'name': data['name'],
        'ticker': ticker,
        'current_price': f"${current_price:.2f}",
        'intrinsic_value': f"${intrinsic_per_share:.2f}",
        'valuation_signal': signal
    })

if __name__ == "__main__":
    results = []
    df = load_tickers(CSV_FILE)
    
    for _, row in df.iterrows():
        evaluate_stock(row, results)
    
    # Save results to CSV
    filename = get_results_filename()
    fieldnames = ['date', 'name', 'ticker', 'current_price', 'intrinsic_value', 'valuation_signal']
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nResults saved to {filename}")
