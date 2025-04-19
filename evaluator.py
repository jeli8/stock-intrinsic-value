import yfinance as yf
import logging
from datetime import datetime
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('financial_evaluator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_financials(ticker):
    logger.info(f"Starting financial data fetch for ticker: {ticker}")
    try:
        stock = yf.Ticker(ticker)
        logger.debug(f"Successfully created Ticker object for {ticker}")
        info = stock.info
        logger.debug(f"Retrieved basic info for {ticker}")

        # Get cashflow statement and its period
        cashflow_stmt = stock.cashflow
        if cashflow_stmt.empty:
            logger.error(f"No cashflow data available for {ticker}")
            return None

        # Debug print the available cashflow statement fields
        logger.debug(f"Available cashflow fields for {ticker}: {cashflow_stmt.index.tolist()}")

        # Get period information
        period_end = cashflow_stmt.columns[0]
        period_start = cashflow_stmt.columns[-1]
        logger.info(f"Cashflow data period for {ticker}: from {period_start.strftime('%Y-%m-%d')} to {period_end.strftime('%Y-%m-%d')}")

        # Try different possible field names for operating cash flow
        operating_cash_flow_fields = [
            'Total Cash From Operating Activities',
            'Operating Cash Flow',
            'Cash Flow From Operations',
            'Net Cash Provided By Operating Activities'
        ]

        cashflow = None
        used_field = None
        for field in operating_cash_flow_fields:
            try:
                if field in cashflow_stmt.index:
                    cashflow = cashflow_stmt.loc[field][0]
                    used_field = field
                    break
            except Exception as e:
                logger.debug(f"Field {field} not found or error: {str(e)}")

        if cashflow is None:
            logger.error(f"Could not find operating cash flow for {ticker} in any known field names")
            return None

        logger.debug(f"{ticker} Operating Cash Flow ({used_field}): ${cashflow:,.2f}")

        # Try to get capital expenditures with different possible field names
        capex_fields = [
            'Capital Expenditures',
            'Capital Expenditure',
            'Purchase Of Plant Property And Equipment',
            'CAPEX'
        ]

        capex = None
        used_capex_field = None
        for field in capex_fields:
            try:
                if field in cashflow_stmt.index:
                    capex = cashflow_stmt.loc[field][0]
                    used_capex_field = field
                    break
            except Exception as e:
                logger.debug(f"Field {field} not found or error: {str(e)}")

        if capex is None:
            logger.error(f"Could not find capital expenditures for {ticker} in any known field names")
            return None

        logger.debug(f"{ticker} Capital Expenditures ({used_capex_field}): ${capex:,.2f}")

        # Calculate FCF
        fcf = cashflow + capex  # Note: capex is usually negative in statements
        logger.debug(f"{ticker} Free Cash Flow: ${fcf:,.2f}")

        # Get current price and shares
        try:
            current_price = info['currentPrice']
            shares_outstanding = info['sharesOutstanding']
            logger.debug(f"{ticker} Current Price: ${current_price:.2f}")
            logger.debug(f"{ticker} Shares Outstanding: {shares_outstanding:,}")
        except KeyError as e:
            logger.error(f"Missing required price/shares data for {ticker}: {str(e)}")
            return None

        result = {
            "fcf": fcf,
            "price": current_price,
            "shares": shares_outstanding,
            "name": info.get('longName', ticker),
            "data_period_end": period_end.strftime("%Y-%m-%d"),
            "data_period_start": period_start.strftime("%Y-%m-%d"),
            "operating_cash_flow_field": used_field,
            "capex_field": used_capex_field
        }
        
        logger.info(f"Successfully fetched all financial data for {ticker}")
        return result

    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}", exc_info=True)
        return None
