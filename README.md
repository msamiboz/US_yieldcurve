# US Yield Curve PCA Analysis & Bond Portfolio Strategy

## Project Overview

This project analyzes the US Treasury yield curve using Principal Component Analysis (PCA) to extract three key factors that drive bond market movements: **Level**, **Slope**, and **Butterfly (Curvature)**. The ultimate goal is to construct a superior bond portfolio using short, medium, and long-term bond ETFs that outperforms traditional total bond market ETFs.

## Theoretical Background

### PCA in Fixed Income
The yield curve can be decomposed into three primary factors:
- **Level (PC1)**: Parallel shifts in the entire yield curve (~80-90% of variance)
- **Slope (PC2)**: Steepening/flattening between short and long rates (~5-15% of variance)  
- **Butterfly/Curvature (PC3)**: Changes in curve curvature (~2-5% of variance)

### Investment Thesis
By understanding these factors and their dynamics, we can:
1. Build targeted exposures using duration-specific ETFs
2. Dynamically rebalance based on factor loadings
3. Potentially achieve better risk-adjusted returns than broad bond indices

## Project Roadmap

### Phase 1: Data Collection and Preparation
1. **Yield Curve Data**
   - Collect historical US Treasury yield data for various maturities
   - Clean and preprocess the data
   - Handle missing values and outliers
   - Create time series dataset

2. **ETF Data**
   - Collect historical price data for:
     - Short-term Treasury ETF: SHY
     - Medium-term Treasury ETF: IEI
     - Long-term Treasury ETFs: TLH
     - Total Bond Market ETF: AGG
   - Calculate daily returns
   - Align dates with yield curve data

### Phase 2: PCA Analysis
1. **Yield Curve Decomposition**
   - Perform PCA on yield curve data
   - Extract first three principal components
   - Calculate explained variance ratio
   - Visualize components and their loadings

2. **Factor Analysis**
   - Interpret PC1 as Level factor
   - Interpret PC2 as Slope factor
   - Interpret PC3 as Butterfly/Curvature factor
   - Create factor time series

### Phase 3: Portfolio Construction
1. **Factor Exposure Analysis**
   - Calculate factor loadings for each ETF
   - Analyze historical factor exposures
   - Identify optimal duration buckets

2. **Portfolio Strategy**
   - Design portfolio allocation rules based on factor signals
   - Implement dynamic rebalancing logic
   - Calculate transaction costs and slippage

### Phase 4: Backtesting and Performance Analysis
1. **Strategy Implementation**
   - Backtest portfolio strategy
   - Compare against benchmark (Total Bond Market ETF)
   - Calculate key performance metrics:
     - Total return
     - Sharpe ratio
     - Maximum drawdown
     - Information ratio

2. **Risk Analysis**
   - Analyze factor risk contributions
   - Calculate portfolio volatility
   - Stress test under different market conditions

### Phase 5: Documentation and Reporting
1. **Results Documentation**
   - Document methodology and assumptions
   - Create performance attribution analysis
   - Generate visualizations and charts

2. **Code Documentation**
   - Document code structure and functions
   - Create usage examples
   - Add inline comments

## Project Structure
```
US_yieldcurve/
├── data/                    # Data storage
│   ├── raw/                # Raw data files
│   └── processed/          # Processed data files
├── notebooks/              # Jupyter notebooks for analysis
├── src/                    # Source code
│   ├── data/              # Data collection and processing
│   ├── analysis/          # PCA and factor analysis
│   ├── portfolio/         # Portfolio construction
│   └── utils/             # Utility functions
├── tests/                  # Unit tests
├── results/               # Analysis results and visualizations
└── docs/                  # Documentation
```

## Getting Started
1. Clone the repository
2. Install required dependencies
3. Run data collection scripts
4. Execute analysis notebooks
5. Review results and documentation

## Dependencies
- Python 3.8+
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- yfinance (for ETF data)
- fredapi (for Treasury data)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

# US_yieldcurve
 
