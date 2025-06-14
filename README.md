# US Yield Curve PCA Analysis & Bond Portfolio Strategy

## Project Overview

This project analyzes the US Treasury yield curve using Principal Component Analysis (PCA) to extract three key factors that drive bond market movements: **Level**, **Slope**, and **Butterfly (Curvature)**. The ultimate goal is to construct a superior bond portfolio using short, medium, and long-term bond ETFs that outperforms traditional total bond market ETFs.

## Investment Thesis

The strategy is based on the following principles:
1. The yield curve can be decomposed into three principal components that explain most of the variance
2. These components have distinct economic interpretations and can be traded independently
3. By dynamically allocating between short, medium, and long-term Treasury ETFs based on these factors, we can potentially achieve better risk-adjusted returns than a static allocation

## Methodology

### Data Collection
- US Treasury yield curve data from FRED
- ETF price data for:
  - SHY (Short-term Treasury)
  - IEI (Medium-term Treasury)
  - TLH (Long-term Treasury)
  - GOVT (Benchmark - Total Treasury Market)

### Factor Analysis
1. **PCA Decomposition**
   - Extract three principal components from yield curve data
   - Interpret components as Level, Slope, and Butterfly factors
   - Calculate factor loadings for each ETF

2. **Signal Generation**
   - Calculate z-scores for each factor using 20-day lookback
   - Generate trading signals based on z-score thresholds
   - Combine signals with factor loadings to determine portfolio weights

3. **Portfolio Construction**
   - Implement dynamic rebalancing with 0.1% threshold
   - Normalize weights to ensure portfolio is fully invested
   - Calculate daily returns and performance metrics

## Results

### Performance Metrics (2015-2024)
| Metric | Portfolio | Benchmark (GOVT) |
|--------|-----------|------------------|
| Annual Return | 4.19% | -0.82% |
| Annual Volatility | 5.16% | 5.29% |
| Sharpe Ratio | 0.81 | -0.15 |
| Tracking Error | 1.66% | - |
| Information Ratio | 3.02 | - |

### Key Findings
1. **Outperformance**: The strategy outperformed the benchmark by 3.55% annually
2. **Risk Management**: Lower volatility than benchmark (5.01% vs 5.29%)
3. **Risk-Adjusted Returns**: Positive Sharpe ratio (0.55) vs negative benchmark (-0.15)
4. **Active Management**: Information ratio of 1.11 indicates consistent outperformance

### Factor Contributions
- Level factor explains ~80% of yield curve variance
- Slope factor explains ~15% of variance
- Butterfly factor explains ~5% of variance

## Future Work

### Interactive Dashboard Development
1. **Portfolio Analysis Dashboard**
   - Real-time performance visualization
   - Interactive factor analysis plots
   - Dynamic weight allocation viewer
   - Performance attribution analysis
   - Custom date range selection

2. **Strategy Customization Interface**
   - User-defined ETF selection
   - Customizable lookback periods
   - Adjustable rebalancing thresholds
   - Factor signal threshold customization

### Data Collection Enhancement
1. **Automated ETF Data Collector**
   - Direct integration with financial data providers
   - Real-time data updates(daily)
   - Support for custom ETF selection
   - Data quality validation

2. **Flexible ETF Selection**
   - Allow users to select their own:
     - Short-term Treasury ETFs
     - Medium-term Treasury ETFs
     - Long-term Treasury ETFs
     - Benchmark ETFs

3. **Deatils of ETFs**
   - ETF metadata and characteristics display
   - ETF comparison tools

### Bias Analysis and Mitigation
1. **Lookahead Bias Prevention**
   - Factor loading is the best candidate

