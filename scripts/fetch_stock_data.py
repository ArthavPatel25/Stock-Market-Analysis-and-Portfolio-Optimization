import yfinance as yf
import pandas as pd
import numpy as np

# List of stock symbols and the time frame for data collection
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
start_date = "2019-01-01"
end_date = "2024-03-01"

# Download historical stock data from Yahoo Finance
stock_data = yf.download(stocks, start=start_date, end=end_date)

# Select the 'Close' price for further analysis
stock_data = stock_data["Close"]

# Reshape data for CSV export: flatten the DataFrame and rename columns
stock_data = stock_data.reset_index().melt(id_vars=["Date"], var_name="stock_symbol", value_name="adjusted_close")
stock_data = stock_data.rename(columns={"Date": "stock_date"})

# Calculate daily return percentage for each stock
stock_data['daily_return'] = stock_data.groupby('stock_symbol')['adjusted_close'].pct_change()

# Compute annualized expected return and volatility for each stock
metrics = stock_data.groupby('stock_symbol').agg({
    'daily_return': [
        lambda x: ((1 + x.mean()) ** 252 - 1),  # Annualized Expected Return
        lambda x: (x.std() * np.sqrt(252))      # Annualized Volatility
    ]
}).reset_index()

# Simplify multi-level column names for clarity
metrics.columns = ['stock_symbol', 'expected_return', 'volatility']

# Calculate the Sharpe Ratio, assuming a risk-free rate of 2%
risk_free_rate = 0.02
metrics['sharpe_ratio'] = (metrics['expected_return'] - risk_free_rate) / metrics['volatility']

# Merge calculated metrics back into the main stock dataset
final_data = pd.merge(stock_data, metrics, on="stock_symbol", how="left")

# Export the final dataset to a CSV file
final_data.to_csv('data/updated_stock_data.csv', index=False)

print("CSV file 'updated_stock_data.csv' successfully updated with calculated metrics!")