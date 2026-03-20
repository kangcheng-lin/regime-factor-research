# Regime Factor Research

This project studies regime-dependent behavior of asset pricing factors using a Hidden Markov Model (HMM). The goal is to rebuild and analyze regime-based factor investing ideas from academic literature and evaluate how factor performance varies across different market conditions.

## Overview

Factor returns are not stationary and can exhibit significantly different behavior under different market regimes. This project:

- Identifies market regimes using an HMM based on returns and volatility
- Integrates standard factor datasets (MKT, SMB, HML, MOM) along with Quality Minus Junk (QMJ)
- Evaluates factor performance conditionally across regimes
- Produces summary statistics and visualizations to compare regime-dependent behavior

## Key Findings

We observe strong regime dependence in factor performance:

- **Market (MKT-RF)**  
  - High Sharpe ratio in bull (low-volatility) regimes  
  - Negative Sharpe in bear regimes  

- **Momentum (MOM)**  
  - Performs well in bull regimes  
  - Underperforms in bear regimes  
  - Consistent with known *momentum crash* behavior  

- **SMB and HML**  
  - Weaker and less consistent regime dependence  

- **Quality (QMJ)**  
  - Positive performance in neutral regimes  
  - **Strongest Sharpe in bear regimes**  
  - Suggests quality may serve as a defensive factor  

### Main Insight

Momentum and quality exhibit complementary behavior:

> Momentum performs best in bull regimes but breaks down in bear regimes, while QMJ remains resilient and performs strongest during market stress.

This supports the idea of **regime-aware factor allocation**.

## Methodology

### 1. Regime Identification
- Hidden Markov Model (HMM)
- Inputs:
  - Daily returns
  - Rolling volatility
- Output:
  - Discrete regimes (bull, neutral, bear)

### 2. Factor Integration
- Fama-French factors:
  - MKT-RF, SMB, HML
- Momentum (MOM)
- AQR Quality Minus Junk (QMJ)

### 3. Regime-Based Analysis
For each regime, we compute:

- Mean return  
- Standard deviation  
- Sharpe ratio  

Results are saved to:

```text
data/results/
├── factor_summary_by_regime.csv
├── sharpe_by_regime.csv
```

## Visualization

### SPY Price with HMM Regimes
![Regimes](plots/spy_regimes.png)

### Factor Sharpe by Regime
![Sharpe](plots/sharpe_by_regime.png)

## Data Sources

- **S&P 500 ETF / market proxy**
  - Yahoo Finance (for OHLC price history used in regime-feature construction)

- **Kenneth French Data Library**
  - Main library:
    - https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
  - Fama/French factors:
    - https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html
  - Momentum factor:
    - Daily:
      - https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor_daily.html
    - Monthly:
      - https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library/det_mom_factor.html

- **AQR Data Library (Quality Minus Junk, QMJ)**
  - Dataset index:
    - https://www.aqr.com/Insights/Datasets
  - QMJ Daily:
    - https://www.aqr.com/Insights/Datasets/Quality-Minus-Junk-Factors-Daily
  - QMJ Monthly:
    - https://www.aqr.com/Insights/Datasets/Quality-Minus-Junk-Factors-Monthly
