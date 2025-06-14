import pandas as pd
from portcreate_functions import *
import pdb 

etf_prices = pd.read_csv('etf_data/all_etfs.csv', index_col=0, parse_dates=True)
etf_returns = etf_prices.pct_change().dropna()

benchmark_returns = etf_returns[['GOVT']].squeeze()
etf_returns = etf_returns[['SHY','IEI','TLH']]



pca_components = 4
lookback_period = 20
rebalance_threshold = 0.001


pca_components= pd.read_csv('pca_components.csv',index_col=0,parse_dates=True)

pca_components.columns= ["Level","Slope","Butterfly"]
pca_components = pca_components.pct_change().dropna()

common_dates = etf_returns.index.intersection(pca_components.index)
etf_returns = etf_returns.loc[common_dates]
pca_components = pca_components.loc[common_dates]



portfolio = construct_portfolio(etf_returns, pca_components, lookback_period, rebalance_threshold)

factor_loadings = calculate_factor_loadings(etf_returns, pca_components)

factor_signals = create_factor_signals(pca_components,lookback_period)

weights = calculate_portfolio_weights(factor_signals, factor_loadings)

weights = implement_rebalancing(weights, rebalance_threshold)

portfolio_returns = calculate_portfolio_returns(weights, etf_returns)

########################################################

# Calculate cumulative returns for portfolio and benchmark
portfolio_cum_returns = (1 + portfolio_returns).cumprod() - 1
benchmark_cum_returns = (1 + benchmark_returns).cumprod() - 1

# Calculate key performance metrics
portfolio_mean = portfolio_returns.mean() * 252  # Annualized return
benchmark_mean = benchmark_returns.mean() * 252
portfolio_vol = portfolio_returns.std() * (252 ** 0.5)  # Annualized volatility  
benchmark_vol = benchmark_returns.std() * (252 ** 0.5)
portfolio_sharpe = portfolio_mean / portfolio_vol  # Sharpe ratio
benchmark_sharpe = benchmark_mean / benchmark_vol


print("\nPortfolio vs Benchmark Performance Metrics:")
print(f"Portfolio Annual Return: {portfolio_mean:.2%}")
print(f"Benchmark Annual Return: {benchmark_mean:.2%}")
print(f"Portfolio Annual Volatility: {portfolio_vol:.2%}")
print(f"Benchmark Annual Volatility: {benchmark_vol:.2%}")
print(f"Portfolio Sharpe Ratio: {portfolio_sharpe:.2f}")
print(f"Benchmark Sharpe Ratio: {benchmark_sharpe:.2f}")

# Calculate tracking error
tracking_error = (portfolio_returns - benchmark_returns).std() * (252 ** 0.5)
print(f"Tracking Error vs Benchmark: {tracking_error:.2%}")

# Calculate information ratio
active_return = portfolio_mean - benchmark_mean
information_ratio = active_return / tracking_error
print(f"Information Ratio: {information_ratio:.2f}")

# Add to port_build.py after calculating all metrics
import json

# Save portfolio results
portfolio_results = {
    'performance_metrics': {
        'portfolio_annual_return': float(portfolio_mean),
        'benchmark_annual_return': float(benchmark_mean),
        'portfolio_annual_volatility': float(portfolio_vol),
        'benchmark_annual_volatility': float(benchmark_vol),
        'portfolio_sharpe_ratio': float(portfolio_sharpe),
        'benchmark_sharpe_ratio': float(benchmark_sharpe),
        'tracking_error': float(tracking_error),
        'information_ratio': float(information_ratio)
    },
    'parameters': {
        'lookback_period': lookback_period,
        'rebalance_threshold': rebalance_threshold
    }
}

# Save results to JSON
import os

# Create results directory if it doesn't exist
os.makedirs('results', exist_ok=True)

with open('results/portfolio_results.json', 'w') as f:
    json.dump(portfolio_results, f, indent=4)

# Save cumulative returns
portfolio_cum_returns.to_csv('results/portfolio_cumulative_returns.csv', index=True)
benchmark_cum_returns.to_csv('results/benchmark_cumulative_returns.csv', index=True)




