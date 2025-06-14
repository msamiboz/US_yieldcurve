import pandas as pd
from sklearn.linear_model import LinearRegression
import pdb

def calculate_factor_loadings(etf_returns, pca_components):
    """
    Calculate how each ETF responds to the three PCA factors
    etf_returns: DataFrame with ETF returns (SHY, IEI, TLH)
    pca_components: DataFrame with the three PCA components (Level, Slope, Butterfly)
    """
    # Run regression for each ETF against the three factors
    factor_loadings = {}
    for etf in ['SHY', 'IEI', 'TLH']:
        # Run multiple regression
        X = pca_components  # Your three PCA components
        y = etf_returns[etf]
        model = LinearRegression()
        model.fit(X, y)
        
        # Store the coefficients (factor loadings)
        factor_loadings[etf] = {
            'Level': model.coef_[0],
            'Slope': model.coef_[1],
            'Butterfly': model.coef_[2]
        }
    
    return pd.DataFrame(factor_loadings)

def create_factor_signals(pca_components, lookback_period=20):
    """
    Create trading signals based on factor movements
    lookback_period: Number of days to look back for signal generation
    """
    signals = pd.DataFrame(index=pca_components.index)
    
    # Calculate rolling statistics for each factor
    for factor in ['Level', 'Slope', 'Butterfly']:
        # Calculate z-score of factor
        rolling_mean = pca_components[factor].rolling(lookback_period).mean()
        rolling_std = pca_components[factor].rolling(lookback_period).std()
        z_score = (pca_components[factor] - rolling_mean) / rolling_std
        
        # Generate signals based on z-score thresholds
        signals[f'{factor}_signal'] = 0
        signals.loc[z_score > 1, f'{factor}_signal'] = 1  # Strong positive signal
        signals.loc[z_score < -1, f'{factor}_signal'] = -1  # Strong negative signal
    
    return signals


def calculate_portfolio_weights(factor_signals, factor_loadings):
    """
    Calculate portfolio weights based on factor signals and loadings
    """
    weights = pd.DataFrame(index=factor_signals.index)
    
    # Initialize weights for each ETF
    for etf in ['SHY', 'IEI', 'TLH']:
        weights[etf] = 1/3
        
        # Calculate weight based on factor signals and loadings
        for factor in ['Level', 'Slope', 'Butterfly']:
            signal = factor_signals[f'{factor}_signal']
            loading = factor_loadings[etf][factor]
            
            # Add to weight based on signal and loading
            weights[etf] += signal * loading
    
    
    # Normalize weights to sum to 1
    weights = weights.div(weights.abs().sum(axis=1), axis=0)
    
    
    return weights

def implement_rebalancing(weights, threshold=0.1):
    """
    Implement rebalancing logic to reduce trading frequency
    threshold: Minimum weight change to trigger rebalancing
    """
    rebalanced_weights = weights.copy()
    last_weights = None
    #pdb.set_trace()
    for date in weights.index:
        if last_weights is None:
            # First day - use initial weights
            last_weights = pd.Series([1/3, 1/3, 1/3], index=['SHY', 'IEI', 'TLH'])
            rebalanced_weights.loc[date] = last_weights
            continue
        
        if weights.loc[date].isna().any():
            # If any NaN, use equal weights
            current_weights = pd.Series([1/3, 1/3, 1/3], index=['SHY', 'IEI', 'TLH'])
            rebalanced_weights.loc[date] = current_weights
            last_weights = current_weights
        else:
            current_weights = weights.loc[date]
            # Check if weight changes exceed threshold
            weight_changes = sum(abs(current_weights - last_weights))
            if weight_changes > threshold:
                # Rebalance
                rebalanced_weights.loc[date] = current_weights
                last_weights = current_weights
            else:
                # Keep previous weights
                rebalanced_weights.loc[date] = last_weights
    
    return rebalanced_weights
    """
    Implement rebalancing logic to reduce trading frequency
    threshold: Minimum weight change to trigger rebalancing
    """
    rebalanced_weights = weights.copy()
    last_weights = None
    
    for date in weights.index:
        if last_weights is None:
            # First day - use initial weights
            last_weights = pd.Series([1/3, 1/3, 1/3], index=['SHY', 'IEI', 'TLH'])
            rebalanced_weights.loc[date] = last_weights
            continue
        
        if weights.loc[date].isna().any():
            current_weights = pd.Series([1/3, 1/3, 1/3], index=['SHY', 'IEI', 'TLH'])
            continue
        else:
            current_weights = weights.loc[date]
        
        # Check if weight changes exceed threshold
        weight_changes = abs(current_weights - last_weights)
        if (weight_changes > threshold).any():
            # Rebalance
            rebalanced_weights.loc[date] = current_weights
            last_weights = current_weights
        else:
            # Keep previous weights
            rebalanced_weights.loc[date] = last_weights
    
    return rebalanced_weights

def calculate_portfolio_returns(weights, etf_returns):
    """
    Calculate portfolio returns based on weights and ETF returns
    """
    # Calculate daily portfolio returns
    portfolio_returns = pd.Series(index=weights.index)
    
    for date in weights.index:
        if date in etf_returns.index:
            # Calculate weighted return
            daily_return = (weights.loc[date] * etf_returns.loc[date]).sum()
            portfolio_returns[date] = daily_return
    
    return portfolio_returns


def construct_portfolio(etf_returns, pca_components, lookback_period=20, rebalance_threshold=0.1):
    """
    Main function to construct and manage the portfolio
    """
    # Step 1: Calculate factor loadings
    factor_loadings = calculate_factor_loadings(etf_returns, pca_components)
    
    # Step 2: Create factor signals
    factor_signals = create_factor_signals(pca_components, lookback_period)
    
    # Step 3: Calculate initial weights
    weights = calculate_portfolio_weights(factor_signals, factor_loadings)
    
    # Step 4: Implement rebalancing
    rebalanced_weights = implement_rebalancing(weights, rebalance_threshold)
    
    # Step 5: Calculate portfolio returns
    portfolio_returns = calculate_portfolio_returns(rebalanced_weights, etf_returns)
    
    return {
        'weights': rebalanced_weights,
        'returns': portfolio_returns,
        'factor_loadings': factor_loadings,
        'signals': factor_signals
    }