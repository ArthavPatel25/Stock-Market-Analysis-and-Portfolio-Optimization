import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import scipy.optimize as sco

# Database connection details
DATABASE_URL = "postgresql://postgres:Arthav_2513@localhost:5432/Stock_Market"

# Establish connection to PostgreSQL database
engine = create_engine(DATABASE_URL)

# Retrieve stock prices from the database
query = "SELECT stock_symbol, stock_date, adjusted_close FROM stock_prices"
df = pd.read_sql(query, engine)

# Reshape the data to have dates as rows and stock symbols as columns
df_pivot = df.pivot(index="stock_date", columns="stock_symbol", values="adjusted_close")

# Calculate daily returns for each stock
returns = df_pivot.pct_change().dropna()

# Function to calculate portfolio return and volatility
def portfolio_performance(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights) * 252
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    return portfolio_return, portfolio_volatility

# Function to compute negative Sharpe ratio for minimization
def negative_sharpe_ratio(weights, returns, risk_free_rate=0.02):
    portfolio_return, portfolio_volatility = portfolio_performance(weights, returns)
    return -(portfolio_return - risk_free_rate) / portfolio_volatility

# Function to optimize portfolio for maximum Sharpe ratio
def optimize_portfolio(returns):
    num_assets = len(returns.columns)
    args = (returns,)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_weights = np.array(num_assets * [1. / num_assets])
    result = sco.minimize(negative_sharpe_ratio, initial_weights, args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x

# Run portfolio optimization
optimal_weights = optimize_portfolio(returns)
expected_return, expected_volatility = portfolio_performance(optimal_weights, returns)
sharpe_ratio = -negative_sharpe_ratio(optimal_weights, returns)

# Display optimal allocation and metrics
print("Optimal Portfolio Allocation:")
for stock, weight in zip(returns.columns, optimal_weights):
    print(f"{stock}: {weight:.2%}")

print(f"\nExpected Annual Return: {expected_return:.2%}")
print(f"Expected Volatility: {expected_volatility:.2%}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# Generate and plot the Efficient Frontier
num_portfolios = 5000
results = np.zeros((3, num_portfolios))
weights_record = []

for i in range(num_portfolios):
    weights = np.random.dirichlet(np.ones(len(returns.columns)), size=1).flatten()
    weights_record.append(weights)
    portfolio_return, portfolio_volatility = portfolio_performance(weights, returns)
    results[0, i] = portfolio_return
    results[1, i] = portfolio_volatility
    results[2, i] = portfolio_return / portfolio_volatility

plt.figure(figsize=(10, 6))
plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap="viridis", alpha=0.6)
plt.colorbar(label="Sharpe Ratio")
plt.xlabel("Volatility (Standard Deviation)")
plt.ylabel("Expected Return")
plt.title("Efficient Frontier")
plt.scatter(expected_volatility, expected_return, c="red", marker="*", s=200, label="Optimal Portfolio")
plt.legend()
plt.grid()
plt.show()
plt.show(block=True)
