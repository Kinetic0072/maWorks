# maWorks - Advanced Computational Trading & Market Simulation System

A professional-grade computational trading simulator demonstrating financial market simulation, algorithmic trading strategies, predictive analytics, and risk management in a university-level computational modeling project.

## 📊 Project Overview

**maWorks** is an AI-powered trading and market simulation platform that combines:
- Real-time market simulation with historical data analysis
- Algorithmic trading strategies (Moving Averages, RSI, MACD, Volume Analysis)
- Machine learning-based price prediction
- Comprehensive risk management
- Professional trading dashboard with interactive visualizations
- Backtesting engine with performance analytics

## 🎯 Core Features

### Market Analysis & Simulation
- Historical market data processing and analysis
- Real-time market simulation engine
- Bull/bear/sideways market scenarios
- Volatility modeling and simulation
- Time-series analysis and forecasting

### Trading Strategies
- **Hybrid Strategy**: Combines multiple technical indicators
  - Moving Average Crossover (Golden Cross/Death Cross)
  - Relative Strength Index (RSI)
  - MACD (Moving Average Convergence Divergence)
  - Volume Analysis
  - Price Action Confirmation

### AI & Predictive Analytics
- LSTM Neural Networks for trend prediction
- Linear Regression forecasting
- Random Forest ensemble methods
- Anomaly detection
- Adaptive strategy optimization

### Risk Management
- Dynamic stop-loss calculation
- Take-profit targets
- Position sizing (2% risk rule)
- Drawdown monitoring
- Spread and slippage simulation
- Portfolio balance tracking

### Performance Analytics
- Backtesting engine with comprehensive metrics
- Profit/Loss analysis
- Win rate and trade accuracy
- Sharpe ratio calculation
- Maximum drawdown tracking
- Trade execution logs

### Professional Dashboard
- Interactive candlestick charts
- Real-time moving average overlays
- Buy/Sell signal visualization
- Portfolio performance metrics
- Risk exposure dashboard
- AI prediction panel
- Market sentiment indicators
- Performance heatmaps

## 🛠️ Technology Stack

```
Core Framework:
- Python 3.9+
- Streamlit (UI framework)

Data & Analysis:
- Pandas (data manipulation)
- NumPy (numerical computing)
- yfinance (market data)
- TA-Lib (technical indicators)

Visualization:
- Plotly (interactive charts)
- Matplotlib (additional visualizations)

Machine Learning:
- Scikit-learn (ML algorithms)
- TensorFlow/Keras (LSTM networks)

Database:
- SQLite (data storage)

Utilities:
- Requests (API calls)
- Scipy (statistical functions)
```

## 📁 Project Structure

```
maWorks/
├── README.md
├── requirements.txt
├── config.py                    # Configuration settings
├── data/
│   ├── market_data.db          # SQLite database
│   └── historical/             # Historical market data
├── src/
│   ├── __init__.py
│   ├── market_simulator.py      # Market simulation engine
│   ├── data_processor.py        # Data loading and preprocessing
│   ├── indicators.py            # Technical indicator calculations
│   ├── trading_strategy.py      # Trading strategy implementation
│   ├── backtester.py           # Backtesting engine
│   ├── ml_predictor.py         # Machine learning models
│   ├── risk_manager.py         # Risk management system
│   └── utils.py                # Utility functions
├── dashboard/
│   ├── app.py                  # Main Streamlit dashboard
│   ├── pages/
│   │   ├── 📊_overview.py      # Market overview page
│   │   ├── 📈_trading.py       # Trading dashboard
│   │   ├── 🤖_ai_prediction.py # AI predictions
│   │   ├── 📉_backtesting.py   # Backtesting results
│   │   └── ⚙️_settings.py      # Configuration
│   ├── components/
│   │   ├── charts.py           # Chart generation
│   │   ├── metrics.py          # Performance metrics
│   │   └── visualizations.py   # Custom visualizations
│   └── styles/
│       └── dashboard.css        # Custom styling
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   ├── model_training.ipynb
│   └── strategy_analysis.ipynb
├── tests/
│   ├── test_indicators.py
│   ├── test_strategy.py
│   └── test_backtester.py
└── docs/
    ├── INSTALLATION.md
    ├── USAGE.md
    ├── API.md
    └── STRATEGY.md
```

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Kinetic0072/maWorks.git
cd maWorks
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run dashboard/app.py
```

### Running Backtests

```bash
python src/backtester.py --symbol AAPL --start-date 2023-01-01 --end-date 2024-01-01
```

## 📊 Dashboard Features

### Market Overview
- Real-time price charts with candlestick visualization
- Moving average crossovers (50/200 MA)
- Volume analysis and trends
- Market sentiment indicators
- Technical indicator overlays

### Trading Dashboard
- Live trading simulation interface
- Entry and exit signal generation
- Position management
- Real-time account balance
- Trade history and logs
- Open positions tracker

### AI Prediction Panel
- LSTM-based price predictions
- Trend forecasting (up/down/neutral)
- Confidence scores
- Anomaly alerts
- Model performance metrics

### Backtesting Engine
- Strategy performance comparison
- Historical trade analysis
- Performance metrics visualization
- Drawdown charts
- Win/Loss distribution
- Strategy parameter optimization

### Risk Management Panel
- Portfolio risk exposure
- Value at Risk (VaR) calculation
- Maximum drawdown tracking
- Stop-loss placement
- Position sizing recommendations
- Risk/Reward ratio analysis

## 📈 Trading Strategy Details

### Entry Signals (BUY)
1. Short MA (20) crosses above Long MA (200) - **Golden Cross**
2. RSI confirms bullish momentum (> 40, not overbought)
3. Price breaks above resistance level
4. Volume increases on breakout
5. Market trend is confirmed bullish

### Exit Signals (SELL)
1. Short MA (20) crosses below Long MA (200) - **Death Cross**
2. RSI indicates overbought (> 70) or bearish divergence
3. Price breaks below support level
4. Volume surge indicates panic selling
5. Market trend weakens or reverses

### Risk Rules
- **Position Size**: Based on 2% risk per trade
- **Stop Loss**: Calculated from entry price and volatility
- **Take Profit**: Set at risk/reward ratio (1:2 minimum)
- **Max Drawdown**: Monitor portfolio-level drawdown
- **Spread/Slippage**: Realistic trading costs included

## 🧠 AI/ML Components

### Models Implemented
- **LSTM Neural Network**: Sequence prediction for price trends
- **Linear Regression**: Trend line analysis
- **Random Forest**: Pattern recognition and anomaly detection
- **Decision Trees**: Decision support for trading signals

### Features
- Automated model training
- Hyperparameter optimization
- Cross-validation and backtesting
- Prediction confidence scoring
- Ensemble methods for robustness

## 📊 Performance Metrics

### Trade Metrics
- **Profit/Loss (P&L)**: Total and per-trade
- **Win Rate**: Percentage of profitable trades
- **Trade Accuracy**: Signal accuracy percentage
- **Average Win/Loss**: Mean winning vs losing trade

### Portfolio Metrics
- **Sharpe Ratio**: Risk-adjusted returns
- **Sortino Ratio**: Downside risk-adjusted returns
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Calmar Ratio**: Return vs drawdown ratio
- **Return on Equity (ROE)**: Total return percentage

### Risk Metrics
- **Volatility**: Standard deviation of returns
- **Value at Risk (VaR)**: Portfolio risk at confidence level
- **Correlation**: Asset correlation analysis
- **Beta**: Market sensitivity

## 🔄 Backtesting Engine

### Capabilities
- Multi-year historical backtests
- Strategy performance comparison
- Parameter optimization (grid search, Bayesian)
- Monte Carlo simulations
- Walk-forward analysis
- Out-of-sample testing

### Output
- Comprehensive performance reports
- Trade-by-trade analysis
- Equity curve visualization
- Drawdown analysis
- Trade distribution analysis

## 🛡️ Risk Management Features

### Position Management
- Automated position sizing
- Risk per trade capping
- Portfolio-level exposure limits
- Dynamic stop-loss adjustment

### Market Protection
- Market circuit breaker rules
- Volatility-based position reduction
- Correlation-based risk hedging
- Liquidity checks before entry

### Monitoring
- Real-time P&L tracking
- Margin monitoring
- Exposure alerts
- Risk threshold notifications

## 📚 Educational Value

This project demonstrates:
- **Computational Modeling**: Market simulation and time-series analysis
- **Financial Engineering**: Strategy design and risk management
- **Data Science**: Statistical analysis and machine learning
- **Software Engineering**: Professional architecture and testing
- **Visualization**: Professional dashboard design
- **Optimization**: Parameter tuning and strategy improvement

## 🔐 Data & Privacy

- Local data storage via SQLite
- No sensitive personal information required
- Simulated trading (no real money involved)
- Historical market data via yfinance API
- Optional data export functionality

## 📖 Documentation

Comprehensive documentation available in `/docs/`:
- **INSTALLATION.md**: Setup and environment configuration
- **USAGE.md**: Feature walkthroughs and examples
- **API.md**: Function reference and module documentation
- **STRATEGY.md**: Detailed strategy documentation

## 🧪 Testing

Unit tests for all core modules:
```bash
pytest tests/ -v
```

## 📝 License

This project is open-source for educational purposes.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional trading strategies
- Advanced ML models (Transformers, GANs)
- Real broker integration
- Multi-asset portfolio management
- Advanced risk analytics

## 📧 Contact

For questions or suggestions, open an issue on GitHub.

---

**Disclaimer**: This is an educational project for computational modeling. Trading involves significant risk. Past performance does not guarantee future results. Never trade with real money without professional financial advice.
