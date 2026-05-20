# Configuration Settings for maWorks Trading System

import os
from datetime import datetime, timedelta

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

APP_NAME = "maWorks - Trading & Market Simulation System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Professional-grade computational trading simulator"

# ============================================================================
# MARKET DATA SETTINGS
# ============================================================================

# Default stock symbols
DEFAULT_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]
WATCHLIST_SYMBOLS = ["SPY", "QQQ", "DIA", "IWM"]

# Data fetch settings
DATA_INTERVAL = "1d"  # 1-minute, 5-minute, 15-minute, 1-hour, 1-day
DEFAULT_LOOKBACK_DAYS = 365
MAX_LOOKBACK_DAYS = 3650

# ============================================================================
# TECHNICAL INDICATORS SETTINGS
# ============================================================================

# Moving Averages
SHORT_MA_PERIOD = 20
LONG_MA_PERIOD = 200
MEDIUM_MA_PERIOD = 50

# RSI (Relative Strength Index)
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# MACD (Moving Average Convergence Divergence)
MACD_FAST_PERIOD = 12
MACD_SLOW_PERIOD = 26
MACD_SIGNAL_PERIOD = 9

# Bollinger Bands
BB_PERIOD = 20
BB_STD_DEV = 2

# Volume
VOLUME_SMA_PERIOD = 20

# ============================================================================
# TRADING STRATEGY SETTINGS
# ============================================================================

# Initial capital
INITIAL_CAPITAL = 100000
TRANSACTION_COST = 0.001  # 0.1% commission

# Position sizing
RISK_PER_TRADE = 0.02  # 2% risk per trade
POSITION_SIZE_METHOD = "kelly"  # kelly, fixed, dynamic

# Entry signals
BUY_CONDITIONS = {
    "ma_crossover": True,
    "rsi_confirmation": True,
    "volume_confirmation": True,
    "price_action": True,
}

# Exit signals
SELL_CONDITIONS = {
    "ma_death_cross": True,
    "rsi_overbought": True,
    "take_profit": True,
    "stop_loss": True,
}

# Risk management
STOP_LOSS_METHOD = "atr"  # atr, fixed_percent, volatility
STOP_LOSS_PERCENT = 0.05  # 5%
STOP_LOSS_ATR_MULTIPLIER = 2.0

TAKE_PROFIT_METHOD = "atr"  # atr, risk_ratio, fixed_percent
TAKE_PROFIT_PERCENT = 0.10  # 10%
TAKE_PROFIT_RISK_RATIO = 2.0  # 1:2 risk-reward ratio
TAKE_PROFIT_ATR_MULTIPLIER = 3.0

# Maximum drawdown
MAX_DRAWDOWN_PERCENT = 0.20  # 20% stop trading if exceeded

# ============================================================================
# MACHINE LEARNING SETTINGS
# ============================================================================

# Model types
ML_MODELS = {
    "lstm": {
        "enabled": True,
        "lookback_window": 60,
        "hidden_units": 64,
        "dropout_rate": 0.2,
        "epochs": 50,
        "batch_size": 32,
    },
    "linear_regression": {
        "enabled": True,
        "lookback_window": 60,
    },
    "random_forest": {
        "enabled": True,
        "n_estimators": 100,
        "max_depth": 10,
        "lookback_window": 60,
    },
    "decision_tree": {
        "enabled": True,
        "max_depth": 10,
        "lookback_window": 60,
    },
}

# Prediction settings
PREDICTION_HORIZON = 5  # Predict next 5 days
CONFIDENCE_THRESHOLD = 0.60  # Minimum confidence to act on prediction
MODEL_RETRAINING_INTERVAL = 30  # Retrain every 30 days

# ============================================================================
# BACKTESTING SETTINGS
# ============================================================================

# Backtest parameters
BACKTEST_START_DATE = "2023-01-01"
BACKTEST_END_DATE = "2024-01-01"
BACKTEST_INITIAL_CAPITAL = 100000

# Optimization
OPTIMIZE_STRATEGIES = True
OPTIMIZATION_METRIC = "sharpe_ratio"  # sharpe_ratio, total_return, win_rate
PARAMETER_OPTIMIZATION_METHOD = "grid"  # grid, bayes, random

# Monte Carlo
MONTE_CARLO_SIMULATIONS = 1000
MONTE_CARLO_PERCENTILE = 95

# ============================================================================
# RISK MANAGEMENT SETTINGS
# ============================================================================

# Portfolio risk
MAX_DAILY_LOSS = 0.05  # 5% daily stop loss
MAX_OPEN_POSITIONS = 5
MAX_POSITION_SIZE_PERCENT = 0.10  # 10% per position
MIN_LIQUIDITY_RATIO = 2.0

# Correlation limits
MAX_CORRELATION_WITH_PORTFOLIO = 0.7
CORRELATION_LOOKBACK_DAYS = 60

# Value at Risk (VaR)
VAR_CONFIDENCE_LEVEL = 0.95
VAR_LOOKBACK_DAYS = 250

# ============================================================================
# SIMULATION SETTINGS
# ============================================================================

# Market simulation
SIMULATION_TYPES = ["bull", "bear", "sideways", "high_volatility"]
SIMULATION_DURATION_DAYS = 252  # 1 year

# Slippage
SLIPPAGE_PERCENT = 0.002  # 0.2%
SLIPPAGE_VOLATILITY_ADJUSTMENT = True

# Spread
SPREAD_PERCENT = 0.001  # 0.1%
SPREAD_TYPE = "percentage"  # percentage or fixed_pip

# ============================================================================
# DATABASE SETTINGS
# ============================================================================

# SQLite database
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "data", "market_data.db")
DATABASE_ECHO = False

# Data retention
DATA_RETENTION_DAYS = 3650  # Keep 10 years of data
AUTO_CLEANUP = True

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

# Chart settings
CHART_THEME = "plotly_dark"
CANDLESTICK_WIDTH = 1
VOLUME_CHART_HEIGHT = 200

# Colors
COLOR_SCHEME = {
    "up": "#00CC96",  # Green for bullish
    "down": "#EF553B",  # Red for bearish
    "neutral": "#636EFA",  # Blue for neutral
    "buy_signal": "#00FF00",
    "sell_signal": "#FF0000",
    "support": "#FFA500",
    "resistance": "#FFA500",
}

# ============================================================================
# DASHBOARD SETTINGS
# ============================================================================

# Page configuration
DASHBOARD_LAYOUT = "wide"
DASHBOARD_THEME = "dark"
PAGE_ICON = "📊"

# Refresh intervals
LIVE_UPDATE_INTERVAL = 60  # seconds
CHART_UPDATE_INTERVAL = 300  # seconds
DATA_FETCH_INTERVAL = 3600  # seconds (1 hour)

# ============================================================================
# PERFORMANCE METRICS SETTINGS
# ============================================================================

# Calculation settings
RISK_FREE_RATE = 0.04  # 4% annual risk-free rate
TRADING_DAYS_PER_YEAR = 252

# Metric thresholds
MIN_SHARPE_RATIO = 1.0
MIN_WIN_RATE = 0.45
MAX_DRAWDOWN_LIMIT = 0.25

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "logs/maworks.log"
LOG_MAX_SIZE = 10485760  # 10 MB
LOG_BACKUP_COUNT = 5

# ============================================================================
# API SETTINGS
# ============================================================================

# Yahoo Finance
YFINANCE_TIMEOUT = 30
YFINANCE_RETRIES = 3

# External APIs
USE_EXTERNAL_APIs = False
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")

# ============================================================================
# NOTIFICATION SETTINGS
# ============================================================================

ENABLE_NOTIFICATIONS = True
NOTIFICATION_TYPES = ["console", "email", "webhook"]

# Email notifications
EMAIL_ENABLED = False
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587
EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Feature engineering
FEATURE_ENGINEERING = True
FEATURE_SCALING = "minmax"  # minmax, standard, robust
FEATURE_SELECTION = True

# Ensemble methods
USE_ENSEMBLE = True
ENSEMBLE_WEIGHTS = {
    "lstm": 0.4,
    "linear_regression": 0.2,
    "random_forest": 0.3,
    "decision_tree": 0.1,
}

# Reinforcement Learning (future)
USE_RL_AGENT = False
RL_TRAINING_EPISODES = 1000

# ============================================================================
# ENVIRONMENT
# ============================================================================

DEBUG_MODE = False
PRODUCTION = False
ENVIRONMENT = "development"  # development, testing, production

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
